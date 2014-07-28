import oboe

def get_template_filename(func, f_args, f_kwargs, res):
    kv = {}

    template_obj = f_args[0]

    if template_obj and hasattr(template_obj, 'filename'):
        kv['filename'] = template_obj.filename

    return kv

from chameleon.zpt.template import PageTemplate

orig_render = PageTemplate.render
template_wrapper = oboe.log_method('chameleon', store_args=False, store_backtrace=False, callback=get_template_filename)
PageTemplate.render = template_wrapper(orig_render)
