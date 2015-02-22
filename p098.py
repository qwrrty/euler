#! /usr/bin/env python

# https://projecteuler.net/problem=98
# 
# Given the input file 'words.txt', find words which are are anagrams
# of each other and can both be mapped to square numbers, using the
# same letter/digit mapping. e.g:
#
#     CARE = 1296 = 36^2   (C = 1, A = 2, R = 9, E = 6)
#     RACE = 9216 = 96^2   (C = 1, A = 2, R = 9, E = 6)
#
# Print out the largest such square that can be found this way.
#
# Strategy:
#
# We can eliminate unnecessary work by:
#   1. Skipping any words in the dictionary that have no anagrams.
#   2. Calculating only square numbers for a given word length at
#      a time
#   2. Starting our search from the longest words in the dictionary.
#      Since the objective is only to find the largest square, we
#      may return immediately once it is certain that we cannot find a
#      larger square.
#
# To determine quickly whether a word maps to a given square number,
# we may define a canonical "lexical pattern" for a string by
# iterating over its characters, and replacing each unseen one with A,
# B, C and so on. For example, both the word APPROPRIATE and the
# number 12234235167 map to the pattern ABBCDBCEAFG.
#
# By precalculating a list of square numbers and their lexical patterns,
# we can determine quickly which (if any) squares match the pattern for
# a given word.
#
# To solve:
#
# 1. Read the list of input words.
#     a. Hash the word into an anagram bucket.
#     b. Eliminate any words that have no anagrams in the dictionary.
#
# 2. Iterate over the anagram buckets, starting with the longest word length.
#     a. Calculate the square numbers that have the same number of digits.
#        Group them by lexical pattern.
#     a. Calculate each word's lexical pattern and look up the squares
#        (if any) with the same pattern.
#     b. Loop through each word/square pair, and determine whether
#        the anagrammed word also maps to a square.

import csv
import math
import time

def read_words(infile):
    """Reads words stored in CSV file INFILE.
    Returns a dict of words grouped into anagram buckets.
    """
    words = []
    with open(infile, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            words = words + row
    return words

def collect_anagrams(words):
    """Groups each word in WORDS (a list of strings) into anagram groups.

    Returns a dict in which each key is a string of letters ordered
    alphabetically, and its value is a set of words which all anagram
    to that key.
    """
    anagrams = {}
    for w in words:
        anagram_key = ''.join(sorted(w))
        anagrams.setdefault(anagram_key, set())
        anagrams[anagram_key].add(w)
    return anagrams

def lexical_pattern(s):
    """Returns the lexical pattern represented by string s.

    Note: results are only well-defined for strings with less than 26
    distinct symbols.
    """
    cipher = {}
    nextkey = 0
    pattern = ''
    for sym in s:
        if sym not in cipher:
            cipher[sym] = chr(ord('A') + nextkey)
            nextkey += 1
        pattern += cipher[sym]
    return pattern

def translate(word1, key, word2):
    """Returns the string that word2 maps to, using word1 and key as
    the key for a char-to-char mapping.

    Raises KeyError if word2 includes any characters not in word1.

    It is assumed that the letters in word1 are mapped consistently
    to the chars in key, i.e. that every occurrence of char X in word1
    is mapped to the same char Y in the key. If this is not the case,
    the last mapping found is used.
    """
    key = dict(zip(word1, key))
    return ''.join(key[sym] for sym in word2)

def calculate_squares(ndigits):
    "Returns a list of square numbers which are each NDIGITS long."
    root = int(math.sqrt(10**ndigits - 1))
    squares = []
    while root > 0 and len(str(root*root)) == ndigits:
        squares.append(root*root)
        root -= 1
    return squares

def findmaxsquare(inputfile):
    words = read_words(inputfile)
    all_anagrams = collect_anagrams(words)
    # Select only anagram groups with at least two words.
    all_anagrams = {k: group
                    for (k, group) in all_anagrams.iteritems()
                    if len(group) > 1}

    # Iterate over anagram groups, starting with the longest words,
    # and look for words that map to square numbers.
    maxsq = 0
    lastgroup = None
    cached_squares = {}
    for group in sorted(all_anagrams.keys(), key=len, reverse=True):
        # If we have found at least one word/square match, and have
        # moved on to a shorter group, we're not going to find a larger
        # square and can quit.
        if maxsq > 0 and lastgroup is not None and len(group) < len(lastgroup):
            break
        lastgroup = group
        anagrams = all_anagrams[group]
        # Get a list of square numbers with the same number of digits
        ndigits = len(group)
        if ndigits not in cached_squares:
            cached_squares[ndigits] = calculate_squares(ndigits)
        squares = cached_squares[ndigits]
        matches = [ (word, sq)
                    for word in anagrams for sq in squares
                    if lexical_pattern(word) == lexical_pattern(str(sq)) ]
        # For each word/square match, check whether any of the word's anagrams
        # maps to another square.
        for word, sq in matches:
            for ana in anagrams:
                if word != ana:
                    sq2 = int(translate(word, str(sq), ana))
                    if sq2 in squares:
                        maxsq = max(sq, sq2, maxsq)
    return maxsq


if __name__ == '__main__':
    t1 = time.clock()
    maxsq = findmaxsquare(inputfile='p098_words.txt')
    runtime = time.clock() - t1
    print maxsq
    print runtime
