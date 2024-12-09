from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Form, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_async_session
from .models import Sound, SoundCreate, SoundQuery, SoundUpdate

sounds_router = APIRouter()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

async def create(data: Annotated[SoundCreate, Form()], db: AsyncSession = Depends(get_async_session)):
    db_item = await Sound.create_from_schema(db, data)
    await db.refresh(db_item)
    return db_item

async def update(data: Annotated[SoundUpdate, Form()], db: AsyncSession = Depends(get_async_session)):
    db_item = await Sound.update_from_schema(db, data)
    await db.refresh(db_item)
    return db_item

async def read_all(filter_query: Annotated[FilterParams, Query()], db: AsyncSession = Depends(get_async_session)):

    result = await db.execute(select(Sound).order_by(filter_query.order_by).limit(filter_query.limit).offset(filter_query.offset))
    return result.scalars().all()

async def query_one(data: SoundQuery = Depends(), db: AsyncSession = Depends(get_async_session)):
    query = select(Sound)
    if data.name:
        query = query.where(Sound.name == data.name)
    if data.date_nominated:
        query = query.where(Sound.date_nominated == data.date_nominated)
    if data.date_created:
        query = query.where(Sound.date_created == data.date_created)
    result = await db.execute(query)
    return result.scalars().first()

sounds_router.add_api_route("", create, methods=["POST"],tags=["sounds"], summary="Create a new sound")
sounds_router.add_api_route("", update, methods=["PUT"],tags=["sounds"], summary="Update a sound")
sounds_router.add_api_route("", read_all, methods=["GET"],tags=["sounds"], summary="Read all sounds")
sounds_router.add_api_route("/query", query_one, methods=["GET"],tags=["sounds"], summary="Query one sound")
