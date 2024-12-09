from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateModel(BaseModel):
    name: str
    description: str
    date_nominated: datetime

class UpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date_nominated: Optional[datetime] = None