import oboe


def extract_name(func, f_args, f_kwargs, res):
    kv = {'Name': f_args[0].__name__}
    return kv

from plone.app.layout.viewlets.manager import ViewletBase
ViewletBase.orig_render = ViewletBase.render
vm_wrapper = oboe.profile_function('plone_viewlet', callback=extract_name)
ViewletBase.render = vm_wrapper(ViewletBase.orig_render)
