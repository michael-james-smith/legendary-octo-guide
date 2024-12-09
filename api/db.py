from datetime import datetime
from typing import Generator, Optional

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Field, Session, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings

echo = False
if settings.ENV == "development":
    echo = True
engine = create_async_engine(settings.DATABASE_URL, echo=echo, future=True)

def datetime_now() -> datetime:
    return datetime.now()

class Base(SQLModel):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    created_at: datetime = Field(default_factory=datetime_now)
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    is_active: bool = Field(default=True)
    deleted_at: Optional[datetime] = Field(default=None)

    @classmethod
    async def create_from_schema(cls, db: AsyncSession, schema):
        if hasattr(schema, 'date_created') and schema.date_created:
            setattr(schema, 'date_created', datetime.strptime(schema.date_created, "%Y"))
        if hasattr(schema, 'date_nominated') and schema.date_nominated:
            setattr(schema, 'date_nominated', datetime.strptime(schema.date_nominated, "%Y"))
        instance = cls(**schema.dict())
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance
    
    @classmethod
    async def update_from_schema(cls, db: AsyncSession, schema):
        try:
            instance = await db.get_one(cls, schema.id)
        except NoResultFound:
            return None
        for key, value in schema.dict(exclude_unset=True).items():
            if value != '':
                setattr(instance, key, value)
        await db.commit()
        await db.refresh(instance)
        return instance

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        instance = cls(**kwargs)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    @classmethod
    async def read(cls, db: AsyncSession, id: int):
        result = await db.exec(select(cls).filter(cls.id == id))
        # result = await db.execute(db.query(cls).filter(cls.id == id))
        return result.scalars().first()

    @classmethod
    async def update(cls, db: AsyncSession, id: int, **kwargs):
        result = await db.exec(select(cls).filter(cls.id == id))
        # result = await db.execute(db.query(cls).filter(cls.id == id))
        instance = result.scalars().first()
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            await db.commit()
            await db.refresh(instance)
        return instance

    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        result = await db.execute(db.query(cls).filter(cls.id == id))
        instance = result.scalars().first()
        if instance:
            await db.delete(instance)
            await db.commit()
        return instance

async def get_async_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


def get_sync_session() -> Generator[Session, None, None]: 
    sync_session = sessionmaker(engine)
    with sync_session() as session:
        yield session
