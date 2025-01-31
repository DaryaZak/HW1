from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine#, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.db_url, echo=True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

#async def get_session() -> AsyncSession: #'это кода от чата и импорт AsyncSession тоже, если что удалить
    #async with async_session_maker() as session:
        #yield session