import oboe
from ZODB.Connection import Connection
from ZODB.utils import u64


def extract_obj_info(func, f_args, f_kwargs):
    obj = f_args[1]

    # lets mimic a mongodb flavor query so queries will show up in the list
    query = '{"OID":%s}' % u64(obj._p_oid)
    
    kv =  {'Flavor': 'mongodb',
           'Database': 'main',
           'Collection': obj.__class__.__name__,
           'Query': query
          }

    return f_args, f_kwargs, kv

Connection.orig_setstate = Connection.setstate
ss_wrapper = oboe.log_method('zodb', entry_kvs={'QueryOp': 'setstate'}, before_callback=extract_obj_info)
Connection.setstate = ss_wrapper(Connection.orig_setstate)

commit_wrapper = oboe.log_method('zodb', entry_kvs={'QueryOp': 'commit'})
Connection.orig_commit = Connection.commit
Connection.commit = commit_wrapper(Connection.orig_commit)
