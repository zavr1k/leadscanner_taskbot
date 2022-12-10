from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True)
    username = Column(String(70))

    tasks = relationship(
        'Task', back_populates='user', order_by='Task.created_date')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(200), index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_date = Column(DateTime)

    user = relationship('User', back_populates='tasks')
