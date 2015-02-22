#! /usr/bin/env python

# https://projecteuler.net/problem=59
#
# The message in p059_cipher.txt is an English text that has been
# XOR-encrypted using a key that consists of three lowercase characters
# and repeated throughout the message.  Determine the key, decrypt
# the message, and print the sum of the ASCII values in the text.
#
# ====================
#
# Strategy:
#
# This is principally a brute force decryption task.  We do not know
# exactly how to identify the plaintext -- only that it will include
# the key in its output, and it will be written in English.  We identify
# successful output if more than half the nontrivial words in the
# plaintext can be found in the system's local dictionary.
#
# A naive implementation that uses Python's native bitwise xor to
# decrypt each byte in the message one at a time is very inefficient.
# Profiling shows that this implementation spends about 95% of its
# time in the XOR function.  By packing the message and key into
# 64-bit integer arrays and using numpy.bitwise_xor(), run time is
# improved by a factor of 3x-5x.
#
# hitchcock:twp% python p059.py --slow
# 107359
# 3.221932
#
# hitchcock:twp% python p059.py
# 107359
# 0.745225

import argparse
import csv
import re
import time

import numpy

def read_csv(csvfile):
    """Reads CSV data from an input file and returns a single list
    containing all of the fields.

    Raises ValueError if the input file contains any non-numeric fields.
    """
    data = []
    with open(csvfile, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            data += [ int(x) for x in row ]
    return data

def read_dictionary(dictfile='/usr/share/dict/words'):
    """Reads the contents of the specified dictionary.
    Returns a set of all the dictionary entries found.
    """
    d = set()
    with open(dictfile, 'r') as f:
        for word in f:
            d.add(word.strip())
    return d

class XORDecoder:

    def __init__(self, dictfile=None):
        self._dict = read_dictionary(dictfile) if dictfile else None

    def dictionary(self):
        return self._dict

    def set_dictionary(self, d):
        self._dict = d

    def key_generator(self):
        """Generates all possible three-character lowercase keys.

        Returns a string containing the key on each call to the generator."""
        for a in range(ord('a'), ord('z')+1):
            for b in range(ord('a'), ord('z')+1):
                for c in range(ord('a'), ord('z')+1):
                    yield chr(a) + chr(b) + chr(c)

    @classmethod
    def fast_xor(cls, msg, key):
        """Repeatedly XORs a message with a key.

        message: a list of integer ASCII values
        key: a string of ASCII chars

        Returns a string consisting of each character generated by
        successively XORing elements of the message with the key.
        """
        msglen = len(msg)

        # numpy.bitwise_xor requires the operands to be the same length.
        # If the message is longer than the key, repeat the key until
        # it is long enough.
        # If the key is longer than the message, truncate it.
        xorkey = key
        if msglen > len(key):
            xorkey = key * (msglen / len(key) + 1)
        xorkey = xorkey[:msglen]

        # Pad out the message and the key to a multiple of 8,
        # so we can xor 8 bytes at once.
        data = msg
        if msglen % 8 != 0:
            padding = 8 - msglen % 8
            data = msg + [0] * padding
            xorkey += ''.join([chr(0)] * padding)

        plaintext = numpy.bitwise_xor(
            numpy.frombuffer(bytearray(data), dtype=numpy.dtype('<Q8')),
            numpy.fromstring(xorkey, dtype=numpy.dtype('<Q8'))).tostring()

        return plaintext[:msglen]

    @classmethod
    def slow_xor(cls, msg, key):
        """Repeatedly XORs a message with a key.  This version is
        only used when the --slow option is invoked.

        message: a list of integer ASCII values
        key: a string of ASCII chars

        Returns a string consisting of each character generated by
        successively XORing elements of the message with the key.
        """
        plaintext = ''
        for i in range(len(msg)):
            plaintext += chr(msg[i] ^ ord(key[i % len(key)]))
        return plaintext

    def decipher(self, message, slow=False):
        """Attempts to decipher the message by repeatedly guessing keys.

        Returns the first plaintext string that matches the following
        conditions:

        * The plaintext includes at least two occurrences of the key
        * At least half of the plaintext words at least five letters long
          are found in the dictionary.

        If no plaintext can be found that satisfies these conditions,
        returns None.
        """
        xor_func = XORDecoder.slow_xor if slow else XORDecoder.fast_xor
        for key in self.key_generator():
            cleartext = xor_func(message, key)

            # The cleartext is known to include repeated instances of the key.
            # Skip any possible solutions that do not include the key at least
            # twice.
            if cleartext.lower().count(key) < 2:
                continue

            # The text is expected to consist principally of English
            # words; however, it is not guaranteed that every word in
            # the text is English or that it will be found in the
            # dictionary we have.  Report success if we found at least
            # one dictionary word, and of the cleartext words that are
            # five letters or longer, at least half are found in the
            # dictionary.
            words = re.findall(r'[A-Za-z]+', cleartext)
            longwords = [ w for w in words if len(w) >= 5 ]
            englishwords = [ w for w in longwords if w in self._dict ]
            if englishwords and len(englishwords) >= len(longwords) / 2:
                return cleartext

        # Continuing through the end of the loop means that we did not
        # find any cleartext that satisfied decryption.
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--slow", help='use slow XOR', action='store_true')
    args = parser.parse_args()

    t1 = time.clock()
    xd = XORDecoder(dictfile='/usr/share/dict/words')
    msg = read_csv('p059_cipher.txt')
    s = xd.decipher(msg, args.slow)
    msgsum = sum([ ord(ch) for ch in s ])
    t2 = time.clock()
    print msgsum
    print "{} seconds".format(t2 - t1)

