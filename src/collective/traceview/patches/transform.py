import oboe

from plone.transformchain import zpublisher
orig_applyTransform = zpublisher.applyTransform
transform_wrapper = oboe.log_method('plone_tchain', store_args=False, store_backtrace=False)
zpublisher.applyTransform = transform_wrapper(orig_applyTransform)
