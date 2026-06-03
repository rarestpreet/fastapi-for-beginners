from fastapi import Depends
from typing import Annotated
from sqlmodel import SQLModel
from sqlmodel import create_engine
from sqlmodel import Session

sqlite_url = "sqlite:///database.db"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def create_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


Session = Annotated[Session, Depends(get_session)]
