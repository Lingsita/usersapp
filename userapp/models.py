from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import PasswordType
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))
    active = Column(String(250), nullable=False)
    last_login = Column(String(250), nullable=True)
 
 
# Create an engine that stores data in users.db file.
engine = create_engine('sqlite:///users.db')
 
Base.metadata.create_all(engine)