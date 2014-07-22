import os
import sys
import oboe

from zope.publisher.browser import BrowserView
from Products.PageTemplates.PageTemplate import PageTemplate

plone_tracing = os.environ.get('TRACEVIEW_PLONE_TRACING', False)
ignore_content_types = os.environ.get('TRACEVIEW_IGNORE_CONTENT_TYPES', '').split(';')
ignore_four_oh_four = os.environ.get('TRACEVIEW_IGNORE_FOUR_OH_FOUR', False)

oboe.config['tracing_mode'] = os.environ.get('TRACEVIEW_TRACING_MODE', 'none')
oboe.config['sample_rate'] = float(os.environ.get('TRACEVIEW_SAMPLE_RATE', '0.3'))


def traverse_wrapper(meth):
    """Extract som basic info about the object and view. traverse method
    gives us access to the traversed object"""

    def extract(self, *args, **kwargs):
        try:
            object = meth(self, *args, **kwargs)
            user = self.get('AUTHENTICATED_USER')
            username = user.getUserName()
            if username == 'Anonymous User':
                partition = 'Anonymous'
            else:
                partition = 'Authenticated'

            kv = {'Partition': partition, 'Class': object.__class__}

            # Old school CMF style page template
            if isinstance(object, PageTemplate):
                kv['Action'] = object.getId()
                kv['Template'] = object.pt_source_file()
                parent = object.getParentNode()
                kv['Controller'] = parent.meta_type

            # Z3 style views
            elif isinstance(object, BrowserView):
                kv['Action'] = object.__name__
                if hasattr(object.context, 'meta_type'):
                    kv['Controller'] = object.context.meta_type

            if 'Controller' not in kv:
                kv['Controller'] = 'Unknown'

            oboe.log('info', None, keys=kv, store_backtrace=False)
            return object

        except:
            raise

    return extract


from ZPublisher.BaseRequest import BaseRequest
BaseRequest.orig_traverse = BaseRequest.traverse
BaseRequest.traverse = traverse_wrapper(BaseRequest.orig_traverse)


def context_wrapper(meth):
    """Wraps the publish method in the current oboe context. """

    def add_context(request, *args, **kwargs):
        ev = None
        ctx = None

        xtr = request.get_header('X-TRACE')
        if xtr:
            md = oboe.Metadata.fromString(xtr)
            ctx = oboe.Context(md)
            ctx.set_as_default()
        elif plone_tracing:
            ctx, ev = oboe.Context.start_trace('plone')
            if ctx.is_valid():
                ev.add_info("URL", 'http://' + request['HTTP_HOST'] + request['PATH_INFO'])
                ev.add_info("Method", request['REQUEST_METHOD'])
                ev.add_info("HTTP-Host", request['HTTP_HOST'])
                ev.add_edge(oboe.Context.get_default())
                ctx.report(ev)
                ctx.set_as_default()

        try:
            res = meth(request, *args, **kwargs)

            if plone_tracing and ctx.is_valid(): 
                content_type = res.headers.get('content-type')

                if content_type.find(';') > 0:
                    content_type = content_type[:content_type.find(';')]

                if content_type not in ignore_content_types and not (ignore_four_oh_four and res.status == 404):
                    ev = ctx.create_event('exit', 'plone')
                    ev.add_info("Status", res.status)
                    ev.add_edge(oboe.Context.get_default())
                    ctx.report(ev)

            if oboe.Context.get_default().is_valid():
                oboe.Context.clear_default()
               
            return res

        except:
            raise


    return add_context


from ZPublisher import Publish
Publish.orig_publish = Publish.publish
publish_wrapper = oboe.log_method('zope_publish')

wrapped_publish = publish_wrapper(Publish.orig_publish)
Publish.publish = context_wrapper(wrapped_publish)
