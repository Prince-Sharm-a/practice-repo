from sqlalchemy import create_engine, text, Column, Integer, String, Float, func, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

mysql_url="mysql+pymysql://root:fs@1591983@localhost:3306/sqlalchemy"
engine=create_engine(mysql_url.replace('@','%40',1), echo=True)

conn=engine.connect()
session=sessionmaker(bind=engine)
Base=declarative_base()

class Person(Base):
    __tablename__='people'
    id=Column(Integer,primary_key=True)
    name=Column(String(20),nullable=False)
    age=Column(Integer,nullable=False)
    
    things=relationship('Thing',back_populates='person')
    
class Thing(Base):
    __tablename__='things'
    id=Column(Integer,primary_key=True)
    description=Column(String(50),nullable=False)
    value=Column(Float)
    owner=Column(Integer,ForeignKey('people.id'))
    
    person=relationship('Person',back_populates='things')

Base.metadata.create_all(engine)

conn=engine.connect()
conn.execute(text("""CREATE TABLE IF NOT EXISTS people(name varchar(20) not null,age int not null)"""))
conn.execute(text('insert into people (name,age) values("Aditya",20);'))
conn.commit()

from sqlalchemy.orm import Session
session = Session(engine)
# session.execute(text('insert into people (name,age) values("Prince",20);'))
# session.commit()