import ujson

from example_response import LONG_TERM_ARTISTS


class Artist(object):

    __slots__ = ['id', 'name', 'genres']

    def __init__(self, id, name, genres):
        self.id = id
        self.name = name
        self.genres = genres

    def __str__(self):
        return str(self.id)


class TaxonomyGraph(object):

    __slots__ = ['nodes', 'edges']

    ROOT_ID = 'root'

    def __init__(self):
        root_node = Node(self.ROOT_ID)
        self.nodes = {root_node.id: root_node}

    def get_root_node(self):
        return self.nodes[self.ROOT_ID]

    def add_node(self, id):
        if id in self.nodes:
            raise Exception('Graph already contains node with ID {}'.format(id))

        new_node = Node(id)
        self.nodes[id] = new_node

        return new_node

    def get_node(self, id):
        if id in self.nodes:
            return self.nodes[id]
        else:
            return None

    def add_edge(self, first_node, second_node):
        '''
        first_node = self.get_node(first_node_id) # or self.add_node(first_node_id)
        second_node = self.get_node(second_node_id) # or self.add_node(second_node_id)
        '''
        first_node.add_neighbor(second_node)

    def __contains__(self, node_id):
        return node_id in self.nodes

    def __iter__(self):
        return iter(self.nodes.values())


class Node(object):

    def __init__(self, id):
        self.id = id
        self.neighbors = set()

    def add_neighbor(self, other_node):
        self.neighbors.add(other_node)

    def get_neighbors(self):
        return list(self.neighbors)

    def __str__(self):
        return str(self.id) + ' connected_to: ' + str([neighbor.id for neighbor in self.neighbors])


def parse_artists_from_spotify_response(spotify_response):
    spotify_artists = spotify_response['items']
    return [_parse_artist_from_spotify_artist(artist) for artist in spotify_artists]


def _parse_artist_from_spotify_artist(spotify_artist):
    return Artist(
        id=spotify_artist['id'],
        name=spotify_artist['name'],
        genres=spotify_artist['genres'],
    )


def build_taxonomy_graph_from_artists(artists):
    taxonomy_graph = TaxonomyGraph()

    for artist in artists:
        artist_slug = artist.name.lower().encode('ascii', 'replace').replace(' ', '-')
        artist_node = taxonomy_graph.add_node(artist_slug)
        genre = artist.genres[0]
        genre_slug = genre.replace(' ', '-')

        if genre_slug not in taxonomy_graph:
            genre_node = taxonomy_graph.add_node(genre_slug)
        else:
            genre_node = taxonomy_graph.get_node(genre_slug)

        taxonomy_graph.add_edge(taxonomy_graph.get_root_node(), genre_node)
        taxonomy_graph.add_edge(genre_node, artist_node)

    return taxonomy_graph


if __name__ == '__main__':
    artists = parse_artists_from_spotify_response(ujson.loads(LONG_TERM_ARTISTS))
    taxonomy_graph = build_taxonomy_graph_from_artists(artists)

    for node in taxonomy_graph:
        for neighbor in node.get_neighbors():
            print '  "{}" -> "{}"'.format(node.id, neighbor.id)
