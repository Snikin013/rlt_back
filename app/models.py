from enum import Enum
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
#from sqlalchemy.orm import Session
#from sqlalchemy.ext.declarative import declarative_base

# from app.config import DATABASE_URL

#Base = declarative_base()

URLDB = "postgresql+psycopg2://admin:admin@46.243.227.152:5432/rlt"


def connect_db():
    db = create_engine(URLDB).connect()    #DATABASE_URL, connect_args={'check_same_thread': False})
    #session = Session(bind=engine.connect())
    return db



