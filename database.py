from sqlalchemy import create_engine,Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker,session
from sqlalchemy.ext.declarative import declarative_base
base=declarative_base()

class notetable(base):
    __tablename__="AISCANNER"
    id=Column(Integer,primary_key=True)
    content=Column(Text)

data_url="postgresql+psycopg://postgres:root%40123@localhost:5432/gurudb"

engine=create_engine(data_url)

Sessionlocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

