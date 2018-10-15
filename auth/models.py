from sqlalchemy import Column, Integer, String

from database_utils import Base


class SpotifyAuthorization(Base):
    __tablename__ = 'spotify_authorization'

    id = Column(Integer, primary_key=True)
    access_token = Column(String(255), nullable=False, index=True)
    refresh_token = Column(String(255), nullable=False)
