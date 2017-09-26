#!/usr/bin/env python

import unittest

from claymoreexporter_lib import validIP,parse_response

class ClaymoreexporterLibTestCase(unittest.TestCase):
    """ Test for claymore-exporter.py"""


    def test_invalid_ip(self):
        """ Is invalid this IP ?"""
        self.assertRaises(ValueError,validIP, '1.2.3.4.5')

    def test_valid_ip(self):
        """ Is valid this IP ?"""
        self.assertEquals(validIP('192.168.1.23'),'192.168.1.23')

    def test_valid_parse_response(self):
        fulltext='{"error": true, "id": 0, "result": ["No client", "6", "0;0;0", "0;0", "0;0;0", "0;0", "0;0;0;0", "-;--", "0;0;0;0"]}'
        received_data = {u'result': [u'No client', u'6', u'0;0;0', u'0;0', u'0;0;0', u'0;0', u'0;0;0;0', u'-;--', u'0;0;0;0'], u'id': 0, u'error': True}
        self.assertEquals(parse_response(fulltext), received_data)

if __name__ == '__main__':
    unittest.main()

