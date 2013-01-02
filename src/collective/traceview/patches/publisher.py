import oboe

from zope.publisher.browser import BrowserView
from Products.PageTemplates.PageTemplate import PageTemplate


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
    """Wraps the publish method in the current oboe context. We need to
    set to context again because it does not survice the transition from
    http server to publisher """

    def add_context(request, *args, **kwargs):
        xtr = request.get_header('X-TRACE')
        if xtr:
            md = oboe.Metadata.fromString(xtr)
            ctx = oboe.Context(md)
            ctx.set_as_default()
        elif oboe.Context.get_default().is_valid():
            oboe.Context.clear_default()        

        try:
            res = meth(request, *args, **kwargs)
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
