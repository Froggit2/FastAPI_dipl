from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///./FastAPI.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)


class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    prise = Column(Integer)


Base.metadata.create_all(bind=engine)