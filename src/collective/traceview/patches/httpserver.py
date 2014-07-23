"""This patch wraps the Zope asyncore based HTTP server. Normally almost all
time would be spend inside the Publisher, but it is interesting to time,
because requests can pile up in ZRendezvous waiting for a worker thread.
"""

import oboe
import os

plone_tracing = os.environ.get('TRACEVIEW_PLONE_TRACING', False)
ignore_content_types = os.environ.get('TRACEVIEW_IGNORE_CONTENT_TYPES', '').split(';')
ignore_four_oh_four = os.environ.get('TRACEVIEW_IGNORE_FOUR_OH_FOUR', False)

oboe.config['tracing_mode'] = os.environ.get('TRACEVIEW_TRACING_MODE', 'none')
oboe.config['sample_rate'] = float(os.environ.get('TRACEVIEW_SAMPLE_RATE', '0.3'))

def handle_request_wrapper(meth):
    def start_trace(self, request):
        ev = None
        ctx = None

        xtr = request.get_header('X-Trace')
        if xtr:
            #md = oboe.Metadata.fromString(xtr)
            #ctx = oboe.Context(md)
            #ctx.set_as_default()
            # set environment
            pass
        elif plone_tracing:
            ctx, ev = oboe.Context.start_trace('zserver_http')
            if ctx.is_valid():
                host = request.get_header('Host')
                uri = request.uri
                command = request.command.upper()

                ev.add_info("URL", 'http://' + host + uri)
                ev.add_info("Method", command)
                ev.add_info("HTTP-Host", host)
                ev.add_edge(oboe.Context.get_default())

                ctx.report(ev)
                ctx.set_as_default()

                xtr = oboe.Metadata.toString(ctx._md)

            if xtr:
                header_line = 'X-Trace: ' + str(xtr)
                request.header = list(request.header) + [header_line]
                request._header_cache = {}

        return meth(self, request)
    return start_trace


def close_response_wrapper(meth):
    def end_trace(self):
        xtr = self._request.get_header('X-Trace')
        if xtr:
            md = oboe.Metadata.fromString(xtr)
            ctx = oboe.Context(md)
            ctx.set_as_default()

            ev = ctx.create_event('exit', 'zserver_http')
            ev.add_info("Status", 200)
            ev.add_edge(oboe.Context.get_default())
            ctx.report(ev)

            oboe.Context.clear_default()            

        return meth(self)

    return end_trace


from ZServer.HTTPServer import zhttp_handler
zhttp_handler.orig_handle_request = zhttp_handler.handle_request
zhttp_handler.handle_request =\
    handle_request_wrapper(zhttp_handler.orig_handle_request)

from ZServer.HTTPResponse import ChannelPipe
ChannelPipe.orig_close = ChannelPipe.close
ChannelPipe.close = close_response_wrapper(ChannelPipe.orig_close)

