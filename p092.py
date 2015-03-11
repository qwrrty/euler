#! /usr/bin/env python

# https://projecteuler.net/problem=92
#
# Square digit chains
#
# A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.
#
# For example,
# 
# 44 -> 32 -> 13 -> 10 -> 1 -> 1
# 85 -> 89 -> 145 -> 42 -> 20 -> 4 -> 16 -> 37 -> 58 -> 89
#
# Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.
#
# How many starting numbers below ten million will arrive at 89?
#
# =====
#
# Strategy: keep a record of each number we encounter and whether it
# eventually goes to 1 to 89.  When checking new numbers, check them
# against this record to avoid recomputing the square digit chain.
# Note that we can save a lot of work by recording the result for each
# intermediate number we generate.

import time

def square_digits(n):
    """Return the sum of the squares of the digits in n."""
    return sum([int(c)**2 for c in str(n)])

def loop(maxn):
    # The "chain" array records the ultimate value (1 or 89) for
    # the square digit chain starting with each index i.
    chain = [0] * (maxn+1)
    chain[1] = 1
    chain[89] = 89
    count_89 = 1
    for n in xrange(1, maxn):
        nums = []
        i = n
        while chain[i] == 0:
            nums.append(i)
            i = square_digits(i)
        # all of the numbers in nums now are known to go to
        # chain[i].
        for j in nums:
            chain[j] = chain[i]
        if chain[n] == 89:
            count_89 += len(nums)

    return count_89

if __name__ == '__main__':
    t1 = time.clock()
    count_89 = loop(10000000)
    t2 = time.clock()
    print count_89
    print "{} seconds".format(t2 - t1)

