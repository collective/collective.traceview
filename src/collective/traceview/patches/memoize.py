import oboe


def extract_cache_key(func, f_args, f_kwargs):
    kv = {'KVOp': 'set',
          'KVKey': f_args[1]}

    return f_args, f_kwargs, kv


def get_wrapper(meth):
    def extract(self, key):
        kv = {'KVOp': 'get', 'KVKey': key}
        oboe.log('entry', 'memoize', keys=kv, store_backtrace=False)

        try:
            val = meth(self, key)
            kv = {'KVHit': True}
            oboe.log('exit', 'memoize', keys=kv, store_backtrace=False)
            return val

        except:
            kv = {'KVHit': False}
            oboe.log('exit', 'memoize', keys=kv, store_backtrace=False)
            raise

    return extract


from plone.memoize.ram import RAMCacheAdapter
orig___setitem__ = RAMCacheAdapter.__setitem__
cache_wrapper = oboe.log_method('memoize', before_callback=extract_cache_key)
RAMCacheAdapter.__setitem__ = cache_wrapper(orig___setitem__)

orig___getitem__ = RAMCacheAdapter.__getitem__
RAMCacheAdapter.__getitem__ = get_wrapper(orig___getitem__)
