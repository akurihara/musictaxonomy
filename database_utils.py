from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///database.db', echo=True)

# Extend this class to create a model backed by a database table.
Base = declarative_base()

# Instantiate this class for an object for performing database operations.
Session = sessionmaker()
Session.configure(bind=engine)
