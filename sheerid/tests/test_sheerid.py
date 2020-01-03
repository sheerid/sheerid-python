import unittest

from sheerid.sheerid import SheerIDRequest


class SheerIDRequestUTF8ParamsTestCase(unittest.TestCase):
    def test_empty_params_should_return_empty_dict(self):
        """
        SheerID request with empty params when converted to utf8_params should return empty dictionary
        """
        req = SheerIDRequest('access_token', 'GET', '/')
        utf8params = req.utf8_params()
        self.assertEqual({}, utf8params)

    def test_non_empty_params_should_return_dict_with_utf8_conversion(self):
        """
        SheerID request with params containing different values (int,float,str,bytes,bytearray,etc.),
        when converted to utf8_params should return dictionary with values converted to UTF-8
        """
        params = {'str_key': 'str_value', 'bytes_key': b'bytes_value',
                  'int_key': 10, 'float_key': 11.22,
                  'bytearray_key': bytearray('bytearray_value', 'utf-8') }
        req = SheerIDRequest('access_token', 'GET', '/', params)
        utf8params = req.utf8_params()
        self.assertEqual({'bytearray_key': 'bytearray_value',
                          'bytes_key': 'bytes_value', 'float_key': 11.22,
                          'int_key': 10, 'str_key': 'str_value'},
                         utf8params)


if __name__ == '__main__':
    unittest.main()
