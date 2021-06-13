from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL_ALCHEMY = os.environ['DATABASE_URL_ALCHEMY']

engine = create_engine(DATABASE_URL_ALCHEMY)
Session = sessionmaker(bind=engine)

Base = declarative_base()