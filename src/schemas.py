from datetime import datetime

from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    user_id: int


class CreateUser(BaseModel):
    user_id: int
    username: str

    class Config:
        orm_mode = True


class Task(CreateTask):
    id: int
    created_date: datetime


class User(CreateUser):
    tasks: list[Task] | None
