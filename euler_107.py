#! /usr/bin/env python

# https://projecteuler.net/problem=107
#
# Using p107_network.txt, a text file containing CSV rows representing
# a weighted network with forty vertices, find the maximum saving
# which can be achieved by removing redundant edges whilst ensuring
# that the network remains connected.
#
# ====================
#
# This problem represents finding a minimal spanning tree for the given
# network.  (Proof: the solution cannot have a higher cost than the minimal
# spanning tree, or else it has not achieved the maximum savings possible
# by remving redundant edges; and the solution cannot have a lower cost
# than a minimal spanning tree, or else it will no longer be fully
# connected.)
#
# This program implements Kruskal's algorithm for finding a minimal
# spanning tree as described in Steven Skiena's "The Algorithm Design
# Manual", section 6.1.2.

import csv
import heapq
import time

class Edge:
    def __init__(self, v1, v2, weight):
        self._v1 = v1
        self._v2 = v2
        self._weight = weight

    def v1(self):
        return self._v1

    def v2(self):
        return self._v2

    def weight(self):
        return self._weight

    def __cmp__(self, other):
        return cmp(self.weight(), other.weight())

    def __repr__(self):
        return "<Edge ({}, {}): {}>".format(self.v1(), self.v2(), self.weight())

class Graph:
    def __init__(self, graphfile=None):
        self._edges = []
        if graphfile is not None:
            self.init_from_file(graphfile)

    def init_from_file(self, graphfile):
        """Initialize a graph using CSV data from graphfile.
        Each row in the input file consists of comma-separated values which
        are either a decimal integer (signifying an edge weight) or the
        string "-".

        The Graph object stores this data as a two-dimensional array of
        cells. The cell at coordinates (i,j) represents the weight of the
        edge between vertices i and j. A weight of 0 means that no edge
        exists between those nodes.
        """
        with open(graphfile, 'r') as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                edges = [ (0 if cell == '-' else int(cell))
                          for cell in row ]
                self._edges.append(edges)

    def num_vertices(self):
        return len(self._edges)

    def set_vertices(self, n):
        self._edges = []
        for i in range(n):
            self._edges.append([0] * n)

    def edge(self, i, j):
        """Returns an Edge object representing the edge between vertices
        i and j, or None if no such edge exists."""
        return (None if self._edges[i][j] == 0
                else Edge(i, j, self._edges[i][j]))

    def add_edge(self, e):
        """Adds edge e to the graph, replacing any edge that may have already
        been present between the specified vertices."""
        self._edges[e.v1()][e.v2()] = e.weight()
        self._edges[e.v2()][e.v1()] = e.weight()

    def edges(self):
        """Generates all edges in the graph, in no particular order.
        Each edge is represented as a tuple (i,j)."""
        for i in range(self.num_vertices()):
            for j in range(self.num_vertices()):
                e = self.edge(i, j)
                if e is not None:
                    yield e

    def total_weight(self):
        return sum([ sum(row) for row in self._edges ]) / 2

def mintree(graph):
    edgequeue = []
    component = range(graph.num_vertices())
    mst = Graph()
    mst.set_vertices(graph.num_vertices())

    # Build a heap of edges by weight.
    for e in graph.edges():
        heapq.heappush(edgequeue, e)
    # Add each edge to the new graph if the components are not connected
    while edgequeue:
        e = heapq.heappop(edgequeue)
        if component[e.v1()] != component[e.v2()]:
            mst.add_edge(e)
            newc = component[e.v1()]
            oldc = component[e.v2()]
            for i in range(len(component)):
                if component[i] == oldc:
                    component[i] = newc
    return mst

if __name__ == '__main__':
    t1 = time.clock()
    g = Graph('p107_network.txt')
    mg = mintree(g)
    savings = g.total_weight() - mg.total_weight()
    t2 = time.clock()
    print savings
    print t2 - t1
