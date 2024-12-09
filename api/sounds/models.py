from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

from ..db import Base


class SoundBase(Base):
    name: str
    description: Optional[str] = None
    date_nominated: Optional[datetime] = None
    date_created: datetime
    audio_file: Optional[str] = None
    image_file: Optional[str] = None
    author: Optional[str] = None

class Sound(SoundBase, table=True):
    __tablename__ = 'sounds'

class SoundCreate(SQLModel):
    name: str
    description: Optional[str] = None
    date_nominated: Optional[str] = None
    date_created: str
    audio_file: Optional[str] = None
    image_file: Optional[str] = None
    author: Optional[str] = None

class SoundQuery(SQLModel):
    name: Optional[str] = None
    date_nominated: Optional[str] = None
    date_created: Optional[str] = None
    pass

class SoundUpdate(SQLModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    date_nominated: Optional[str] = None
    date_created: Optional[str] = None
    audio_file: Optional[str] = None
    image_file: Optional[str] = None
    author: Optional[str] = None