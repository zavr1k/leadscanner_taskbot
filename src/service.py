from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models as m
import schemas as s
from config import MAX_USER_TASKS


def add_user_to_session(user: s.CreateUser, session: AsyncSession) -> m.User:
    """Added telegram user to database"""
    new_user = m.User(**user.dict())
    session.add(new_user)
    return new_user


def add_task_to_session(task: s.CreateTask, session: AsyncSession) -> m.Task:
    """Added task to database"""
    new_task = m.Task(**task.dict(), created_date=datetime.utcnow())
    session.add(new_task)
    return new_task


async def create_user_if_not_exist(
    user_id: int, session: AsyncSession, username: str
) -> None:
    """Added telegram user to database if it does not exist"""
    db_user = await get_user_by_id(user_id=user_id, session=session)
    if not db_user:
        new_user = s.CreateUser(user_id=int(user_id), username=username)
        add_user_to_session(user=new_user, session=session)
        await session.commit()


async def has_task_limit(
    user_id: int, session: AsyncSession, limit=MAX_USER_TASKS
) -> bool:
    """Checks if the user's task limit has been reached"""
    tasks = await session.execute(
        select(m.Task).where(m.Task.user_id == user_id))
    number = len(tasks.scalars().all())
    if number >= limit:
        return False
    return True


async def get_user_by_id(user_id: int, session: AsyncSession) -> s.User | None:
    """Gets user form datatabase by telegram user id"""
    user = await session.execute(
        select(m.User)
        .options(selectinload(m.User.tasks))
        .where(m.User.user_id == user_id))
    user = user.scalars().first()
    if not user:
        return
    tasks = [
        s.Task(id=task.id, user_id=task.user_id, title=task.title,
               created_date=task.created_date)
        for task in user.tasks]
    return s.User(
        user_id=user.user_id,
        username=user.username,
        tasks=tasks)


async def get_user_tasks(
        user_id: int, session: AsyncSession) -> list[s.Task | None]:
    """Gets all user tasks"""
    tasks = await session.execute(
        select(m.Task)
        .where(m.Task.user_id == user_id)
        .order_by(m.Task.created_date))
    tasks = tasks.scalars().all()
    if not tasks:
        return []
    return [
        s.Task(id=task.id, user_id=task.user_id, title=task.title,
               created_date=task.created_date)
        for task in tasks
    ]


async def delete_task(task_id: int, session: AsyncSession) -> None:
    """Delete task by id"""
    await session.execute(delete(m.Task).where(m.Task.id == task_id))
    await session.commit()
