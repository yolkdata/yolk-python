import unittest
import pkgutil
import logging
import sys
import yolk

from yolk.client import Client


def all_names():
    for _, modname, _ in pkgutil.iter_modules(__path__):
        yield 'yolk.test.' + modname


def all():
    logging.basicConfig(stream=sys.stderr)
    return unittest.defaultTestLoader.loadTestsFromNames(all_names())


class TestInit(unittest.TestCase):
    def test_writeKey(self):
        self.assertIsNone(yolk.default_client)
        yolk.flush()
        self.assertEqual(yolk.default_client.write_key, 'test-init')

    def test_debug(self):
        self.assertIsNone(yolk.default_client)
        yolk.debug = True
        yolk.flush()
        self.assertTrue(yolk.default_client.debug)
        yolk.default_client = None
        yolk.debug = False
        yolk.flush()
        self.assertFalse(yolk.default_client.debug)

    def test_gzip(self):
        self.assertIsNone(yolk.default_client)
        yolk.gzip = True
        yolk.flush()
        self.assertTrue(yolk.default_client.gzip)
        yolk.default_client = None
        yolk.gzip = False
        yolk.flush()
        self.assertFalse(yolk.default_client.gzip)

    def test_host(self):
        self.assertIsNone(yolk.default_client)
        yolk.host = 'test-host'
        yolk.flush()
        self.assertEqual(yolk.default_client.host, 'test-host')

    def test_max_queue_size(self):
        self.assertIsNone(yolk.default_client)
        yolk.max_queue_size = 1337
        yolk.flush()
        self.assertEqual(yolk.default_client.queue.maxsize, 1337)

    def test_max_retries(self):
        self.assertIsNone(yolk.default_client)
        client = Client('testsecret', max_retries=42)
        for consumer in client.consumers:
            self.assertEqual(consumer.retries, 42)

    def test_sync_mode(self):
        self.assertIsNone(yolk.default_client)
        yolk.sync_mode = True
        yolk.flush()
        self.assertTrue(yolk.default_client.sync_mode)
        yolk.default_client = None
        yolk.sync_mode = False
        yolk.flush()
        self.assertFalse(yolk.default_client.sync_mode)

    def test_timeout(self):
        self.assertIsNone(yolk.default_client)
        yolk.timeout = 1.234
        yolk.flush()
        self.assertEqual(yolk.default_client.timeout, 1.234)

    def setUp(self):
        yolk.write_key = 'test-init'
        yolk.default_client = None
