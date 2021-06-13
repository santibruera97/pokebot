from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL_ALCHEMY = os.environ['DATABASE_URL_ALCHEMY']
DATABASE_URL_ALCHEMY = 'postgresql://zlwnvtysdtrnyy:c2b5009d836e8703cf3b3493b2d638697287def3b58ee388058d2200efa0b16f@ec2-52-86-25-51.compute-1.amazonaws.com:5432/dq6kknk8r228g'
engine = create_engine(DATABASE_URL_ALCHEMY)
Session = sessionmaker(bind=engine)

Base = declarative_base()