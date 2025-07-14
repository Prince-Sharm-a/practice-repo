from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from model import Person, Thing
from sqlalchemy import func
from model import session,engine
# from schemas.note import notesEntity, noteEntity
from fastapi.templating import Jinja2Templates

note = APIRouter()
templates=Jinja2Templates(directory="template")


@note.get("/",response_class=HTMLResponse)
async def read_item(request: Request):
    # docs=conn.Notes.notes.find({})
    # newDocs=[]
    # for doc in docs:
    #     newDocs.append({
    #         "id":doc["_id"],
    #         "title":doc["title"],
    #         "desc":doc["desc"],
    #         "important":doc["important"]
    #     })    
    newDocs=session.query(Person.name,Person.age,Thing.description,Thing.value).join(Thing).all()
    # newDocs=dict(newDocs)
    return templates.TemplateResponse("index.html",{"request":request,"newDocs":newDocs})



@note.post("/")
async def creat_item(request:Request):
    # NoteDef:Note
    form = await request.form()
    # print(form)
    if form["name"]!='' and form['age']!='':
        newPerson=Person(name=form["name"],age=form["age"])
        session.add(newPerson)
        if form["desc"]!='':
            session.flush()
    if form["desc"]!='' and form['value']!='':
        newThing=Thing(description=form["desc"],value=form["value"],owner=newPerson.id)
        session.add(newThing)
    session.commit()
    return RedirectResponse(url="/",status_code=303)
    # formDict=dict(form)
    # print(formDict)
    # formDict["important"]=True if formDict.get("important")=="on" else False
    # inserted_note=conn.Notes.notes.insert_one(formDict)
    # return {"Sucess":True}

@note.put('/table')
async def update(id:int):
        