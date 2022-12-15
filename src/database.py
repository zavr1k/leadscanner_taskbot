from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Done')


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
