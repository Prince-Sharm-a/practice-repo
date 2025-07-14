from fastapi import FastAPI,APIRouter
from sqlalchemy import create_engine, text
from note import note


app=APIRouter
app.include_router(note)
