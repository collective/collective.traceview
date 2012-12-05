"""This patch wraps the Zope asyncore based HTTP server. Normally almost all
time would be spend inside the Publisher, but it is interesting to time,
because requests can pile up in ZRendezvous waiting for a worker thread.
"""

import oboe


def handle_request_wrapper(meth):
    def start_trace(self, request):
        ctx, ev = oboe.Context.start_trace('zope_http',
                                           xtr=request.get_header('X-Trace'))
        ev.add_info("URL", request.uri)
        ev.add_info("Method", request.command)
        ev.add_info("HTTP-Host", request.get_header('Host'))
        ctx.report(ev)

        # create & store finish event for reporting later
        # we are storing the context and event on the request object
        # because the context disappears from the oboe default approach:
        # thread-local

        request._oboe_ctx = ctx
        # adds edge from exit event -> enter event's md
        request._oboe_finish_ev = ctx.create_event('exit', 'zope_http')

        return meth(self, request)
    return start_trace


def close_response_wrapper(meth):
    def end_trace(self):
        if self._request._oboe_finish_ev and self._request._oboe_ctx and\
           self._request._oboe_ctx.is_valid():
            ev = self._request._oboe_finish_ev
            ctx = self._request._oboe_ctx

            ev.add_edge(oboe.Context.get_default())
            ctx.report(ev)

        self._request._oboe_ctx = None
        self._request._oboe_finish_ev = None
        return meth(self)

    return end_trace


from ZServer.HTTPServer import zhttp_handler
zhttp_handler.orig_handle_request = zhttp_handler.handle_request
zhttp_handler.handle_request =\
    handle_request_wrapper(zhttp_handler.orig_handle_request)

from ZServer.HTTPResponse import ChannelPipe
ChannelPipe.orig_close = ChannelPipe.close
ChannelPipe.close = close_response_wrapper(ChannelPipe.orig_close)
