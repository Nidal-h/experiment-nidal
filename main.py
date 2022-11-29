
from typing import List
from fastapi import FastAPI
import databases

import sqlalchemy

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "postgresql://rbovifsapgrdnx:a13a777891d383da5a438cf33d4186fa1775d4d559d03baf50c7fb0bb0d56557@ec2-54-174-31-7.compute-1.amazonaws.com:5432/dla9e9tffuhs6"

database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(

    "notes",

    metadata,

    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),

    sqlalchemy.Column("username", sqlalchemy.String),

    sqlalchemy.Column("password", sqlalchemy.String),


)



engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)



class Note(BaseModel):
    id: int
    username: str
    password: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)

@app.post("/notes/", response_model=Note)
async def create_note(note: Note):
    query = notes.insert().values(username=note.username, password=note.password)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}