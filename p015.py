#! /usr/bin/env python

# Lattice paths: how many routes are there through a 20x20 grid?
#
# Any given cell (x,y) has (x+1,y) + (x,y+1) routes through the grid.
# If x is at the maximum, (x+1,y) is assumed to be zero.
# Same for when y is at the maximum with (x,y+1).
#
# We can calculate the number of paths non-recursively: start with the
# knowledge that (20,20) will be 1 and work backward.
#
# lattice(19,20) = 1 path
# lattice(20,19) = 1 path
# lattice(19,19) = 2 paths (one to the right and one down)
#
# We can easily calculate each diagonal from lattice(x,20) to lattice(0,20-x).

import pprint

lattice = [0] * 21
for i in range(21):
    lattice[i] = [0] * 21
lattice[20][20] = 1

for col in range(19,0,-1):
    x = col
    y = 20
    while x <= 20:
        countdown = 0 if y == 20 else lattice[x][y+1]
        countright = 0 if x == 20 else lattice[x+1][y]
        lattice[x][y] = countdown + countright
        x += 1
        y -= 1

for row in range(20,0,-1):
    y = row
    x = 0
    while y >= 0:
        countdown = 0 if y == 20 else lattice[x][y+1]
        countright = 0 if x == 20 else lattice[x+1][y]
        lattice[x][y] = countdown + countright
        x += 1
        y -= 1

lattice[0][0] = lattice[1][0] + lattice[0][1]
print lattice[0][0]
