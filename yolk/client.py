from datetime import datetime
from decimal import DefaultContext
from uuid import uuid4
import logging
import numbers
import atexit
import time

from dateutil.tz import tzutc
from six import string_types

from yolk.utils import guess_timezone, clean
from yolk.consumer import Consumer
from yolk.request import post
from yolk.version import VERSION

try:
    import queue
except ImportError:
    import Queue as queue


ID_TYPES = (numbers.Number, string_types)


class Client(object):
    class DefaultConfig(object):
        org = None
        write_key = None
        env = "development"
        ids = None
        appInfo = None
        on_error = None
        debug = False
        send = True
        sync_mode = False
        max_queue_size = 10000
        gzip = False
        timeout = 15
        max_retries = 10
        proxies = None
        thread = 1
        flush_interval = 0.5
        flush_at = 100
        max_retries = 10

    """Create a new Yolk client."""
    log = logging.getLogger('yolk')

    def __init__(self,
                 org=DefaultConfig.org,
                 write_key=DefaultConfig.write_key,
                 env=DefaultConfig.env,
                 ids=DefaultConfig.ids,
                 appInfo=DefaultConfig.appInfo,
                 debug=DefaultConfig.debug,
                 max_queue_size=DefaultConfig.max_queue_size,
                 send=DefaultConfig.send,
                 on_error=DefaultConfig.on_error,
                 gzip=DefaultConfig.gzip,
                 max_retries=DefaultConfig.max_retries,
                 sync_mode=DefaultConfig.sync_mode,
                 timeout=DefaultConfig.timeout,
                 proxies=DefaultConfig.proxies,
                 thread=DefaultConfig.thread,
                 flush_at=DefaultConfig.flush_at,
                 flush_interval=DefaultConfig.flush_interval):
        require('org', org, string_types)
        require('write_key', write_key, string_types)

        self.queue = queue.Queue(max_queue_size)
        self.org = org
        self.write_key = write_key
        self.env = env
        self.ids = ids
        self.appInfo = appInfo
        self.on_error = on_error
        self.debug = debug
        self.send = send
        self.sync_mode = sync_mode
        self.gzip = gzip
        self.timeout = timeout
        self.proxies = proxies

        if debug:
            self.log.setLevel(logging.DEBUG)

        if sync_mode:
            self.consumers = None
        else:
            # On program exit, allow the consumer thread to exit cleanly.
            # This prevents exceptions and a messy shutdown when the
            # interpreter is destroyed before the daemon thread finishes
            # execution. However, it is *not* the same as flushing the queue!
            # To guarantee all messages have been delivered, you'll still need
            # to call flush().
            if send:
                atexit.register(self.join)
            for _ in range(thread):
                self.consumers = []
                consumer = Consumer(
                    self.queue, org, write_key, env, ids, appInfo, on_error=on_error,
                    flush_at=flush_at, flush_interval=flush_interval,
                    gzip=gzip, retries=max_retries, timeout=timeout,
                    proxies=proxies,
                )
                self.consumers.append(consumer)

                # if we've disabled sending, just don't start the consumer
                if send:
                    consumer.start()

    # track an event
    def track(self, data, timestamp=None, context=None):
        context = context or {}
        msg = {
            'type': 'event',
            'timestamp': timestamp,
            'context': context,
            
            'data': {
                'name': data['name'],
                'properties': data['properties'],
                'created': data['created'],
                'type': 'event',
                'id': str(int(time.time())),
            },
        }

        return self._enqueue(msg)

    # tie person to an identifier
    def alias(self, data, timestamp=None, context=None):
        context = context or {}
        msg = {
            'type': 'alias',
            'timestamp': timestamp,
            'context': context,

            'data': {
                'properties': data['properties'],
                'created': data['created'],
                'name': 'alias',
                'type': 'alias',
                'id': str(int(time.time())),
            },
        }

        return self._enqueue(msg)

    def _enqueue(self, msg):
        """Push a new `msg` onto the queue, return `(success, msg)`"""
        timestamp = msg['timestamp']
        if timestamp is None:
            timestamp = datetime.utcnow().replace(tzinfo=tzutc())
        message_id = msg.get('messageId')
        if message_id is None:
            message_id = uuid4()

        # require('integrations', msg['integrations'], dict)
        # require('type', msg['type'], string_types)
        require('timestamp', timestamp, datetime)
        require('context', msg['context'], dict)

        # add common
        timestamp = guess_timezone(timestamp)
        msg['timestamp'] = timestamp.isoformat()
        msg['messageId'] = stringify_id(message_id)
        msg['context']['library'] = {
            'name': 'yolk-python',
            'version': VERSION
        }

        msg['userId'] = stringify_id(msg.get('userId', None))
        msg['anonymousId'] = stringify_id(msg.get('anonymousId', None))

        msg = clean(msg)
        self.log.debug('queueing: %s', msg)
        
        # if send is False, return msg as if it was successfully queued
        if not self.send:
            return True, msg

        if self.sync_mode:
            self.log.debug('enqueued with blocking %s.', msg['type'])
            self.log.debug('enqueued with blocking message %s.', msg)
            post(self.org, self.write_key, self.env, self.ids, self.appInfo, self.gzip,
                 self.proxies, batch=[msg])

            return True, msg

        try:
            self.queue.put(msg, block=False)
            self.log.debug('enqueued %s.', msg['type'])
            return True, msg
        except queue.Full:
            self.log.warning('yolk-python queue is full')
            return False, msg

    def flush(self):
        """Forces a flush from the internal queue to the server"""
        queue = self.queue
        size = queue.qsize()
        queue.join()
        # Note that this message may not be precise, because of threading.
        self.log.debug('successfully flushed about %s items.', size)

    def join(self):
        """Ends the consumer thread once the queue is empty.
        Blocks execution until finished
        """
        for consumer in self.consumers:
            consumer.pause()
            try:
                consumer.join()
            except RuntimeError:
                # consumer thread has not started
                pass

    def shutdown(self):
        """Flush all messages and cleanly shutdown the client"""
        self.flush()
        self.join()


def require(name, field, data_type):
    """Require that the named `field` has the right `data_type`"""
    if not isinstance(field, data_type):
        msg = '{0} must have {1}, got: {2}'.format(name, data_type, field)
        raise AssertionError(msg)


def stringify_id(val):
    if val is None:
        return None
    if isinstance(val, string_types):
        return val
    return str(val)
