from fastapi import APIRouter
from sqlalchemy import create_engine, text

mysql_url="mysql+pymysql://root:fs@1591983@localhost:3306/sqlalchemy"
engine=create_engine(mysql_url.replace('@','%40',1), echo=True)