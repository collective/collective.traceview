import oboe


def extract_template(func, f_args, f_kwargs):
    self = f_args[0]
    kv = {'Template': self.program[2][1]}
    return f_args, f_kwargs, kv

from zope.tal.talinterpreter import TALInterpreter
TALInterpreter.orig_call = TALInterpreter.__call__
template_wrapper = oboe.log_method('zope_template', before_callback=extract_template)
TALInterpreter.__call__ = template_wrapper(TALInterpreter.orig_call)
