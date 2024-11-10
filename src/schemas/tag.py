from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    tag_title: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
