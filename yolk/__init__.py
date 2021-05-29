
from yolk.version import VERSION
from yolk.client import Client

__version__ = VERSION

"""Settings."""
org = Client.DefaultConfig.org
write_key = Client.DefaultConfig.write_key
env = Client.DefaultConfig.env
ids = Client.DefaultConfig.ids
appInfo = Client.DefaultConfig.appInfo
on_error = Client.DefaultConfig.on_error
debug = Client.DefaultConfig.debug
send = Client.DefaultConfig.send
sync_mode = Client.DefaultConfig.sync_mode
max_queue_size = Client.DefaultConfig.max_queue_size
gzip = Client.DefaultConfig.gzip
timeout = Client.DefaultConfig.timeout
max_retries = Client.DefaultConfig.max_retries

default_client = None


def track(*args, **kwargs):
    """Send a track call."""
    _proxy('track', *args, **kwargs)


def alias(*args, **kwargs):
    """Send an alias call."""
    _proxy('alias', *args, **kwargs)


def flush():
    """Tell the client to flush."""
    _proxy('flush')


def join():
    """Block program until the client clears the queue"""
    _proxy('join')


def shutdown():
    """Flush all messages and cleanly shutdown the client"""
    _proxy('flush')
    _proxy('join')


def _proxy(method, *args, **kwargs):
    """Create a yolk client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
        default_client = Client(org,
                                write_key, env, ids, appInfo, debug=debug,
                                max_queue_size=max_queue_size,
                                send=send, on_error=on_error,
                                gzip=gzip, max_retries=max_retries,
                                sync_mode=sync_mode, timeout=timeout)

    fn = getattr(default_client, method)
    fn(*args, **kwargs)
