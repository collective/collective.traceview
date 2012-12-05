import sys
import oboe
from oboe import OboeException
from oboe import log_error

def log_exception(msg=None, store_backtrace=True):
    """Report the last thrown exception as an error

    :msg: An optional message, to override err_msg. Defaults to str(Exception).
    :store_backtrace: Whether to store the Exception backtrace.
    """
    typ, val, tb = sys.exc_info()
    if typ is None:
        raise OboeException('log_exception should only be called from an exception context (e.g., except: block)')
    if msg is None:
        msg = unicode(val).encode('utf8', 'ignore')

    if store_backtrace:
        backtrace = tb
    else:
        backtrace = None

    log_error(typ.__name__, msg, store_backtrace=store_backtrace, backtrace=backtrace)


oboe.log_exception = log_exception
