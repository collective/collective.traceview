import oboe
from ZPublisher.BaseRequest import BaseRequest


wrapper = oboe.profile_function('zope_traverse')
BaseRequest.orig_traverse = BaseRequest.traverse
BaseRequest.traverse = wrapper(BaseRequest.orig_traverse)
