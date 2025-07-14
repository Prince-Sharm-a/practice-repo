from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


mysql_url="mysql+pymysql://root:fs@1591983@localhost:3306/sqlalchemy"
engine=create_engine(mysql_url.replace('@','%40',1), echo=True)

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

Session=sessionmaker(bind=engine)
session=Session()

# new_person=Person(name='luffy',age=59)
# session.add(new_person)
# session.flush()

# new_thing=Thing(description='haki',value=900,owner=new_person.id)
# session.add(new_thing)

# session.commit()

# print([t.description for t in new_person.things])
# print(new_thing.person.name)

result=session.query(Person.name,Person.age).all()
print(result)

result=session.query(Person).filter(Person.age>40).all()
print("Person age greater 40 : ",[(p.name,p.age) for p in result])

result=session.query(Thing).filter(Thing.value<50).all()
print([t.description for t in result])

session.query(Person).filter(Person.name=='luffy').update({'name':'zoro'})
session.commit()

result=session.query(Person.name,Thing.description).join(Thing).all()
print([t for t in result])

result=session.query(Thing.owner,func.sum(Thing.value)).group_by(Thing.owner).having(func.sum(Thing.value)>50).limit(3)
print("only 3: ",[t for t in result])
result=session.query(Thing.owner,func.sum(Thing.value)).group_by(Thing.owner).having(func.sum(Thing.value)>50).all()
print("all: ",[t for t in result])

new_var = 25//7
print(type(new_var))
print(new_var)