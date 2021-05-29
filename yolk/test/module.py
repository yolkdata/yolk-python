import unittest

import yolk


class TestModule(unittest.TestCase):

    # def failed(self):
    #     self.failed = True

    def setUp(self):
        self.failed = False
        yolk.write_key = 'testsecret'
        yolk.on_error = self.failed

    def test_no_write_key(self):
        yolk.write_key = None
        self.assertRaises(Exception, yolk.track)

    def test_no_host(self):
        yolk.host = None
        self.assertRaises(Exception, yolk.track)

    def test_track(self):
        yolk.track('userId', 'python module event')
        yolk.flush()

    def test_identify(self):
        yolk.identify('userId', {'email': 'user@email.com'})
        yolk.flush()

    def test_group(self):
        yolk.group('userId', 'groupId')
        yolk.flush()

    def test_alias(self):
        yolk.alias('previousId', 'userId')
        yolk.flush()

    def test_page(self):
        yolk.page('userId')
        yolk.flush()

    def test_screen(self):
        yolk.screen('userId')
        yolk.flush()

    def test_flush(self):
        yolk.flush()
