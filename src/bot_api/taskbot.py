from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from schemas import CreateTask, CreateUser, Task, User
from service import (add_task_to_session, add_user_to_session, delete_task,
                     get_user_tasks)

router = APIRouter()


@router.post('/user', response_model=User)
async def create_user(
        user: CreateUser,
        session: AsyncSession = Depends(get_session)):
    """Creates user"""
    created_user = add_user_to_session(user=user, session=session)
    await session.commit()
    return created_user


@router.post('/add', response_model=Task)
async def create_task(
        task: CreateTask,
        session: AsyncSession = Depends(get_session)):
    """Creates user's task"""
    created_task = add_task_to_session(task=task, session=session)
    await session.commit()
    return created_task


@router.get('/list/{user_id}', response_model=list[Task | None])
async def get_task_list(
        user_id: int,
        session: AsyncSession = Depends(get_session)):
    """Gets user with his tasks"""
    tasks = await get_user_tasks(user_id=user_id, session=session)
    if not tasks:
        return []
    return tasks


@router.delete('/task/{task_id}')
async def list_task(
        task_id: int, session: AsyncSession = Depends(get_session)):
    """Delete task from database"""
    await delete_task(task_id=task_id, session=session)
