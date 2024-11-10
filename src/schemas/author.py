from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from schemas.tag import Tag


class AuthorBase(BaseModel):
    full_name: str
    country: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: UUID
    books: list[UUID] = Field(default_factory=list)
    tags: list[Tag] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
