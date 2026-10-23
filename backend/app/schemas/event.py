import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    venue: str
    starts_at: datetime
    capacity: int
    status: str
    created_at: datetime
    updated_at: datetime


class EventPage(BaseModel):
    items: list[EventRead]
    total: int
    limit: int
    offset: int
