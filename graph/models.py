from sqlalchemy import Column, Integer, ForeignKey, String

from database_utils import Base


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    spotify_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    spotify_name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)


class ArtistGenre(Base):
    __tablename__ = 'artist_genres'

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)


class TaxonomyGraph(object):

    __slots__ = ['nodes', 'edges']

    ROOT_ID = 'root'

    def __init__(self):
        root_node = Node(self.ROOT_ID)
        self.nodes = {root_node.id: root_node}

    def get_root_node(self):
        return self.nodes[self.ROOT_ID]

    def get_nodes(self):
        return self.nodes.values()

    def get_edges(self):
        return [
            (node, neighbor)
            for node in self.get_nodes()
            for neighbor in node.get_neighbors()
        ]

    def add_node(self, id):
        if id in self.nodes:
            raise Exception('Graph already contains node with ID {}'.format(id))

        new_node = Node(id)
        self.nodes[id] = new_node

        return new_node

    def add_genre_node(self, id):
        if id in self.nodes:
            raise Exception('Graph already contains node with ID {}'.format(id))

        new_node = GenreNode(id)
        self.nodes[id] = new_node

        return new_node

    def add_subgenre_node(self, id, name):
        if id in self.nodes:
            raise Exception('Graph already contains node with ID {}'.format(id))

        new_node = SubgenreNode(id, name)
        self.nodes[id] = new_node

        return new_node

    def add_artist_node(self, id, name):
        if id in self.nodes:
            raise Exception('Graph already contains node with ID {}'.format(id))

        new_node = ArtistNode(id, name)
        self.nodes[id] = new_node

        return new_node

    def get_node(self, id):
        return self.nodes[id] if id in self.nodes else None

    def add_edge(self, first_node, second_node):
        first_node.add_neighbor(second_node)

    def add_genre_to_subgenre_edge(self, genre_node, subgenre_node):
        self.add_edge(genre_node, subgenre_node)
        subgenre_node.set_genre(genre_node.id)

    def add_genre_to_artist_edge(self, genre_node, artist_node):
        self.add_edge(genre_node, artist_node)
        artist_node.set_genre(genre_node.id)

    def add_subgenre_to_artist_edge(self, subgenre_node, artist_node):
        self.add_edge(subgenre_node, artist_node)
        artist_node.set_genre(subgenre_node.genre)

    def render_as_json(self):
        return {
            'nodes': [node.render_as_json() for node in self.get_nodes()],
            'links': [self._render_edge_as_json(edge) for edge in self.get_edges()],
        }

    def _render_edge_as_json(self, edge):
        source_node, destination_node = edge
        return {
            'source': source_node.id,
            'target': destination_node.id,
        }

    def __contains__(self, node_id):
        return node_id in self.nodes

    def __iter__(self):
        return iter(self.nodes.values())


class Node(object):

    __slots__ = ['id', 'neighbors']

    def __init__(self, id):
        self.id = id
        self.neighbors = set()

    def add_neighbor(self, other_node):
        self.neighbors.add(other_node)

    def get_neighbors(self):
        return list(self.neighbors)

    def render_as_json(self):
        return {'id': self.id}

    def __str__(self):
        return str(self.id) + ' connected_to: ' + str([neighbor.id for neighbor in self.neighbors])


class GenreNode(Node):

    __slots__ = ['id', 'name', 'neighbors']

    def __init__(self, id):
        super().__init__(id)
        self.name = id

    def render_as_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class SubgenreNode(Node):

    __slots__ = ['id', 'genre', 'name', 'neighbors']

    def __init__(self, id, name):
        super().__init__(id)
        self.name = name
        self.genre = None

    def set_genre(self, genre):
        self.genre = genre

    def render_as_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class ArtistNode(Node):

    __slots__ = ['id', 'genre', 'name', 'neighbors']

    def __init__(self, id, name):
        super().__init__(id)
        self.name = name
        self.genre = None

    def set_genre(self, genre):
        self.genre = genre

    def render_as_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }
