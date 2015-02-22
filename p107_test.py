#! /usr/bin/env python

import unittest

from p107 import Edge, Graph, mintree

class TestEuler107(unittest.TestCase):

    def test_edges(self):
        "Tests Edge constructors and accessors."
        edge1 = Edge(1, 2, 1000)
        edge2 = Edge(50, 60, 7)
        edge3 = Edge(2, 100, 7)
        self.assertEqual(1,    edge1.v1())
        self.assertEqual(2,    edge1.v2())
        self.assertEqual(1000, edge1.weight())
        self.assertEqual(50,   edge2.v1())
        self.assertEqual(60,   edge2.v2())
        self.assertEqual(7,    edge2.weight())
        self.assertGreater(edge1, edge2)
        self.assertEqual(edge2, edge3)

    def test_graph(self):
        "Tests simple graph building operations."
        g = Graph()
        g.set_vertices(3)
        self.assertEqual(3, g.num_vertices())
        self.assertIsNone(g.edge(0, 1))
        self.assertIsNone(g.edge(1, 2))
        self.assertIsNone(g.edge(0, 2))

        g.add_edge(Edge(0, 1, 1))
        g.add_edge(Edge(1, 2, 5))
        g.add_edge(Edge(0, 2, 2))
        self.assertEqual(Edge(0, 0, 1), g.edge(0, 1))
        self.assertEqual(Edge(0, 0, 5), g.edge(1, 2))
        self.assertEqual(Edge(0, 0, 2), g.edge(0, 2))

        # Test replacing an existing edge.
        g.add_edge(Edge(1, 2, 13))
        self.assertEqual(Edge(0, 0, 13), g.edge(1, 2))

        # Check weights
        self.assertEqual(16, g.total_weight())

    def test_min_spanning_tree(self):
        """Tests that the minimal spanning tree for a simple fully
        connected graph leaves out the expected heaviest edges."""
        g = Graph()
        g.set_vertices(3)
        g.add_edge(Edge(0, 1, 1))
        g.add_edge(Edge(1, 2, 5))
        g.add_edge(Edge(0, 2, 2))

        mg = mintree(g)
        self.assertEqual(Edge(0, 0, 1), mg.edge(0, 1))
        self.assertEqual(Edge(0, 0, 2), mg.edge(0, 2))
        self.assertIsNone(mg.edge(1,2))


if __name__ == '__main__':
    unittest.main()
