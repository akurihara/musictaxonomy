from sqlalchemy import Column, Integer, String

from musictaxonomy.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(255), nullable=False)
    external_source = Column(String(255), nullable=False)
    external_id = Column(Integer, nullable=False)
