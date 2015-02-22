#! /usr/bin/env python

import unittest

import euler_98

class TestEuler98(unittest.TestCase):

    def test_collect_anagrams(self):
        self.assertEqual({}, euler_98.collect_anagrams([]))

        self.assertEqual({'ACT': set(['CAT'])},
                         euler_98.collect_anagrams(['CAT']))

        self.assertEqual({'ACT': set(['CAT', 'ACT'])},
                         euler_98.collect_anagrams(['CAT', 'ACT']))

        self.assertEqual(
            {'OPST': set(['POST', 'SPOT', 'STOP']),
             'OPS':  set(['SOP', 'OPS', 'POS']),
             'OP':   set(['OP'])},
            euler_98.collect_anagrams(
                ['OP', 'OPS', 'POS', 'POST', 'SOP', 'SPOT', 'STOP']))

    def test_lexical_pattern(self):
        self.assertEqual('',            euler_98.lexical_pattern(''))
        self.assertEqual('ABCDEF',      euler_98.lexical_pattern('GARDEN'))
        self.assertEqual('ABCDEF',      euler_98.lexical_pattern('ENGARD'))
        self.assertEqual('ABCDEF',      euler_98.lexical_pattern('123456'))
        self.assertEqual('ABCDEF',      euler_98.lexical_pattern('615423'))
        self.assertEqual('ABCC',        euler_98.lexical_pattern('KNEE'))
        self.assertEqual('ABCC',        euler_98.lexical_pattern('5311'))
        self.assertEqual('ABCADAEABCA', euler_98.lexical_pattern('ABRACADABRA'))

    def test_calculate_squares(self):
        self.assertItemsEqual([], euler_98.calculate_squares(0))
        self.assertItemsEqual([1, 4, 9], euler_98.calculate_squares(1))
        self.assertItemsEqual(
            [16, 25, 36, 49, 64, 81],
            euler_98.calculate_squares(2))
        self.assertItemsEqual(
            [100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400,
             441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961],
            euler_98.calculate_squares(3))

    def test_translate(self):
        # Test edge cases: where word1/key/word2 are all empty strings
        self.assertEqual('', euler_98.translate('', '', ''))
        self.assertEqual('', euler_98.translate('', 'xyz', ''))
        self.assertEqual('', euler_98.translate('abc', '', ''))
        self.assertEqual('', euler_98.translate('abc', 'xyz', ''))

        # Simple translation test
        self.assertEqual(
            'DEALT', euler_98.translate('ALICE', 'DELTA', 'ALEIC'))
        # Translation including digits
        self.assertEqual(
            '17689', euler_98.translate('BROAD', '18769', 'BOARD'))
        # If key and word2 are different lengths, extra chars are ignored
        self.assertEqual(
            'DEALT', euler_98.translate('ALICE', 'DELTAFORCE', 'ALEIC'))
        self.assertEqual(
            'DEALT', euler_98.translate('ALICERESTAURANT', 'DELTA', 'ALEIC'))

        # If word2 references chars not found in word1, it raises an exception
        with self.assertRaises(KeyError):
            euler_98.translate('ABCDE', '12345', 'ABCDX')


if __name__ == '__main__':
    unittest.main()
