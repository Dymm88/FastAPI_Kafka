from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from schemas.author import Author
from schemas.tag import Tag


class BookBase(BaseModel):
    title: str
    genre: str
    created_at: int | None = None


class BookCreate(BookBase):
    author_id: UUID | None = None
    tags: list[UUID] = []


class Book(BookBase):
    id: UUID
    author: Author
    tags: list[Tag] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
