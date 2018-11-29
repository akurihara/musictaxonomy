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

    def render_in_webgraphviz_format(self):
        return ''.join([node.render_edges_in_webgraphviz_format() for node in self])

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

    def render_edges_in_webgraphviz_format(self):
        edges = [
            self._render_edge_in_webgraphviz_format(neighbor)
            for neighbor in self.get_neighbors()
        ]
        return ','.join(edges)

    def _render_edge_in_webgraphviz_format(self, neighbor):
        return '"{}" -> "{}"'.format(self.id, neighbor.id)

    def __str__(self):
        return str(self.id) + ' connected_to: ' + str([neighbor.id for neighbor in self.neighbors])
