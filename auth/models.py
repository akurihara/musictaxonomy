from sqlalchemy import Column, Integer, String

from database_utils import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(255), nullable=False)
    external_source = Column(String(255), nullable=False)
    external_id = Column(Integer, nullable=False)


class SpotifyAuthorization(Base):
    __tablename__ = 'spotify_authorization'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    access_token = Column(String(255), nullable=False, index=True)
    refresh_token = Column(String(255), nullable=False)
