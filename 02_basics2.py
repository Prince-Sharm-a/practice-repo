from sqlalchemy import ForeignKey, create_engine, MetaData, Table, Column, Integer, String, func, insert, Float

mysql_url="mysql+pymysql://root:fs@1591983@localhost:3306/sqlalchemy"
engine=create_engine(mysql_url.replace('@','%40',1), echo=True)

meta=MetaData()

people = Table(
    "people",
    meta,
    Column('id',Integer,primary_key=True),
    Column('name',String(20),nullable=False),
    Column('age',Integer,nullable=False)
)

things = Table(
    "things",
    meta,
    Column('id',Integer,primary_key=True),
    Column('description',String(50),nullable=False),
    Column('value',Float),
    Column('owner',Integer,ForeignKey('people.id'))
)

meta.create_all(engine)

conn=engine.connect()

# insert_statement=people.insert().values(name='Prince',age=20)
# insert_statement=insert(people).values(name='Prince',age=20) # -> another to use insert method

# insert_statement=people.insert().values(name='Fanish',age=40)

# result=conn.execute(insert_statement)
# conn.commit()

select_statement=people.select().where(people.c.age>30)
result=conn.execute(select_statement)
print(result.fetchall())

update_statement=people.update().where(people.c.name=='Fanish').values(age=50)
result=conn.execute(update_statement)

select_statement=people.select()
result=conn.execute(select_statement)
print(result.fetchall())

delete_statement=people.delete().where(people.c.name=='Aditya')
result=conn.execute(delete_statement)
conn.commit()

select_statement=people.select()
result=conn.execute(select_statement)
print(result.fetchall())



# insert_people=people.insert().values([
#     {'name':'Aditya','age':21},
#     {'name':'Vishal','age':22},
#     {'name':'Tushar','age':23},
#     {'name':'Pranav','age':23},
#     {'name':'Naman','age':21},
#     {'name':'Ayush','age':20},
#     {'name':'Akash','age':22},
# ])
# conn.execute(insert_people)
# conn.commit()

# insert_things=things.insert().values([
#     {'owner':1,'description':'Laptop','value':30.22},
#     {'owner':3,'description':'Mobile','value':33.22},
#     {'owner':5,'description':'Ipad','value':43.22},
#     {'owner':7,'description':'Mouse','value':35.22},
#     {'owner':3,'description':'Keyboard','value':40.22},
#     {'owner':1,'description':'Speaker','value':20.22},
#     {'owner':10,'description':'Books','value':22.22},
#     {'owner':8,'description':'Bottle','value':29.22}
# ])
# conn.execute(insert_things)
# conn.commit()

# join_statement=people.join(things,people.c.id==things.c.owner)
# select_statement = things.select().with_only_columns(things.c.description,people.c.name).select_from(join_statement)
# result=conn.execute(select_statement)
# for row in result.fetchall():
#     print(row)

join_statement=people.join(things,people.c.id==things.c.owner)
group_by_statement=things.select().with_only_columns(things.c.owner,people.c.name,func.sum(things.c.value)).select_from(join_statement).group_by(things.c.owner) #.having(func.sum(things.c.value))
result=conn.execute(group_by_statement)
for row in result.fetchall():
    print(row)

