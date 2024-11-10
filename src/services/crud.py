import uuid
from typing import TypeVar, Generic, Type

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateType = TypeVar("CreateType")


class CRUDBase(Generic[ModelType, CreateType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, obj_in: CreateType) -> ModelType:
        obj = self.model(**obj_in.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_all(self) -> list[ModelType]:
        result = await self.session.execute(select(self.model).order_by(self.model.id))
        return result.scalars().all()

    async def get_one(self, obj_id: uuid) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        obj = result.scalars().first()
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        return obj

    async def update(
        self, obj_id: uuid, obj_in: CreateType, partial: bool = False
    ) -> ModelType:
        obj = await self.get_one(obj_id)
        for key, value in obj_in.model_dump(exclude_unset=partial).items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def remove(self, obj_id: uuid) -> str:
        obj = await self.get_one(obj_id)
        await self.session.delete(obj)
        await self.session.commit()
        return f"{self.model.__name__} has been deleted"
