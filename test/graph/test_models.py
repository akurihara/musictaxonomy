from unittest import TestCase

from musictaxonomy.graph.models import Node, TaxonomyGraph


class TaxonomyGraphTest(TestCase):
    def test_add_genre_node_with_duplicate_id(self):
        taxonomy_graph = TaxonomyGraph("John Doe")
        taxonomy_graph.add_genre_node("Rock")

        with self.assertRaises(Exception):
            taxonomy_graph.add_genre_node("Rock")

    def test_add_subgenre_node_with_duplicate_id(self):
        taxonomy_graph = TaxonomyGraph("John Doe")
        taxonomy_graph.add_subgenre_node("indie rock", "Indie Rock")

        with self.assertRaises(Exception):
            taxonomy_graph.add_subgenre_node("indie rock", "Indie Rock")

    def test_add_artist_node_with_duplicate_id(self):
        taxonomy_graph = TaxonomyGraph("John Doe")
        taxonomy_graph.add_artist_node("3TVXtAsR1Inumwj472S9r4", "Drake")

        with self.assertRaises(Exception):
            taxonomy_graph.add_artist_node("3TVXtAsR1Inumwj472S9r4", "Drake")


class NodeTest(TestCase):
    def test_conversion_to_string(self):
        first_node = Node(id="Rock")
        second_node = Node(id="Indie Rock")
        first_node.add_neighbor(second_node)

        self.assertEqual(str(first_node), "Rock connected to: ['Indie Rock']")

    def test_render_as_json(self):
        node = Node(id="Rock")

        self.assertEqual(node.render_as_json(), {"id": "Rock"})
