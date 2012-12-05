import oboe


def extract_name(func, f_args, f_kwargs, res):
    kv = {'Name': f_args[0].__name__}
    return kv

from plone.app.viewletmanager.manager import OrderedViewletManager
OrderedViewletManager.orig_render = OrderedViewletManager.render
vm_wrapper = oboe.profile_function('plone_viewletman', callback=extract_name)
OrderedViewletManager.render = vm_wrapper(OrderedViewletManager.orig_render)
