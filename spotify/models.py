class SpotifyArtist(object):

    __slots__ = ['id', 'name', 'genres']

    def __init__(self, id, name, genres):
        self.id = id
        self.name = name
        self.genres = genres

    def __str__(self):
        return str(self.id)
