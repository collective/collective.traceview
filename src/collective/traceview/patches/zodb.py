import oboe
from ZODB.Connection import Connection
from ZODB.utils import u64


def extract_obj_info(func, f_args, f_kwargs):
    obj = f_args[1]

    # lets mimic a mongodb flavor query so queries will show up in the list
    query = '{"Class":"%s","OID":%s}' % (str(obj.__class__), u64(obj._p_oid))

    kv =  {'Flavor': 'mongodb',
           'QueryOp': 'find',
           'Query': query
          }

    return f_args, f_kwargs, kv

Connection.orig_setstate = Connection.setstate
ss_wrapper = oboe.log_method('zodb', entry_kvs={'Op': 'setstate'}, before_callback=extract_obj_info)
Connection.setstate = ss_wrapper(Connection.orig_setstate)

commit_wrapper = oboe.log_method('zodb', entry_kvs={'Op': 'commit'})
Connection.orig_commit = Connection.commit
Connection.commit = commit_wrapper(Connection.orig_commit)
