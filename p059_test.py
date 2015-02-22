#! /usr/bin/env python

import unittest

from p059 import XORDecoder

class XorTestMixin:

    def test_xor_simple(self):
        """Tests a simple XOR transformation."""
        msg = [2, 13, 20]
        key = 'abc'
        output = self.xor_func(msg, key)
        self.assertEqual(3, len(output))
        self.assertEqual(output[0], chr( 2 ^ ord('a')))
        self.assertEqual(output[1], chr(13 ^ ord('b')))
        self.assertEqual(output[2], chr(20 ^ ord('c')))

    def test_xor_short_key(self):
        """Tests the XOR function with a key shorter than its message."""
        msg = [2, 13, 20, 21, 13, 20, 15]
        key = 'abc'
        output = self.xor_func(msg, key)
        self.assertEqual(7, len(output))
        self.assertEqual(output[0], chr( 2 ^ ord('a')))
        self.assertEqual(output[1], chr(13 ^ ord('b')))
        self.assertEqual(output[2], chr(20 ^ ord('c')))
        self.assertEqual(output[3], chr(21 ^ ord('a')))
        self.assertEqual(output[4], chr(13 ^ ord('b')))
        self.assertEqual(output[5], chr(20 ^ ord('c')))
        self.assertEqual(output[6], chr(15 ^ ord('a')))

    def test_xor_long_key(self):
        """Tests the XOR function with a key longer than its message."""
        msg = [2, 13, 20]
        key = 'abcdefghijklmnopqrstuvwxyz'
        output = self.xor_func(msg, key)
        self.assertEqual(3, len(output))
        self.assertEqual(output[0], chr( 2 ^ ord('a')))
        self.assertEqual(output[1], chr(13 ^ ord('b')))
        self.assertEqual(output[2], chr(20 ^ ord('c')))

    def test_xor_inverse(self):
        """Tests that the XOR transformation is its own inverse."""
        src = 'The quick brown fox'
        key = 'abcdef'
        cipher = self.xor_func([ord(x) for x in src], key)
        self.assertNotEqual(src, cipher)
        output = self.xor_func([ord(x) for x in cipher], key)
        self.assertEqual(src, output)


class SlowXorTests(unittest.TestCase, XorTestMixin):
    def setUp(self):
        self.xor_func = XORDecoder.slow_xor


class FastXorTests(unittest.TestCase, XorTestMixin):
    def setUp(self):
        self.xor_func = XORDecoder.fast_xor


class KeyGeneratorTest(unittest.TestCase):
    def test_key_generator(self):
        """Test that the key generator produces the expected
        number of keys, and test that the first few are what we expect."""
        xd = XORDecoder()
        keys = [ x for x in xd.key_generator() ]
        self.assertEqual(26 * 26 * 26, len(keys))
        self.assertEqual(keys[0], 'aaa')
        self.assertEqual(keys[1], 'aab')
        self.assertEqual(keys[2], 'aac')


class DecipherTest(unittest.TestCase):
    """Test XORDecoder.decipher() calls with a known dictionary."""
    def setUp(self):
        self.xd = XORDecoder()
        self.xd.set_dictionary(
            set("alpha bravo charlie delta echo foxtrot golf hotel".split()))

    def test_decipher_all_words_in_dict(self):
        """Test that decipher() succeeds on a string whose words are all
        found in the dictionary."""
        src = 'alpha bravo foxtrot charlie foxtrot golf hotel'
        key = 'fox'
        data = [ord(x) for x in src]
        cipher = XORDecoder.fast_xor(data, key)
        cipherdata = [ord(x) for x in cipher]
        self.assertEqual(src, self.xd.decipher(cipherdata))

    def test_decipher_half_words_in_dict(self):
        """Test that decipher() succeeds when 50% of the words in the source
        are in the dictionary.
        """
        src = 'alpha bravo foxtrot foxtrot india juliet november oscar'
        key = 'fox'
        data = [ord(x) for x in src]
        cipher = XORDecoder.fast_xor(data, key)
        cipherdata = [ord(x) for x in cipher]
        self.assertEqual(src, self.xd.decipher(cipherdata))

    def test_decipher_few_words_in_dict(self):
        """Test that decipher() fails when less than 50% of the words in
        the source are found in the dictionary."""
        src = 'alpha bravo foxtrot foxtrot india juliet november oscar quebec romeo'
        key = 'fox'
        data = [ord(x) for x in src]
        cipher = XORDecoder.fast_xor(data, key)
        cipherdata = [ord(x) for x in cipher]
        self.assertEqual(None, self.xd.decipher(cipherdata))

    def test_decipher_key_not_in_source(self):
        """Test that decipher() fails when the key is not found at least
        twice in the cleartext."""
        src = 'alpha bravo charlie delta echo foxtrot'
        key = 'fox'
        data = [ord(x) for x in src]
        cipher = XORDecoder.fast_xor(data, key)
        cipherdata = [ord(x) for x in cipher]
        self.assertEqual(None, self.xd.decipher(cipherdata))


if __name__ == '__main__':
    unittest.main()
