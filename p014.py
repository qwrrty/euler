#! /usr/bin/env python

# Collatz numbers: collatz[n-1] is the length of the Collatz sequence
# for n
#
# We can calculate each Collatz sequence recursively: if we don't know
# the length of collatz[n], figure out the term m that follows n, and
# then set collatz[n] to collatz[m] + 1.

collatz = {}
collatz[0] = 1

def find_collatz(n):
    if n-1 not in collatz:
       c = n/2 if n%2==0 else (3*n + 1)
       collatz[n-1] = find_collatz(c) + 1
    return collatz[n-1]

maxc = 1
for i in range(1,1000000):
    c = find_collatz(i)
    if c > collatz[maxc-1]:
        maxc = i

print "{} ({})".format(maxc, collatz[maxc-1])
