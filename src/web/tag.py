from uuid import UUID

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import TagCreate
from services import TagCRUD

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(tag: TagCreate, session: AsyncSession = Depends(db_handler.get_db)):
    return await TagCRUD(session).create(tag)


@router.get("/", response_model=list[TagCreate])
async def get_all(session: AsyncSession = Depends(db_handler.get_db)):
    return await TagCRUD(session).get_all()


@router.get("/{tag_id}", response_model=TagCreate)
async def get_one(tag_id: UUID, session: AsyncSession = Depends(db_handler.get_db)):
    return await TagCRUD(session).get_one(tag_id)


@router.put("/{tag_id}", response_model=TagCreate, status_code=status.HTTP_202_ACCEPTED)
async def update(
    tag_id: UUID, tag: TagCreate, session: AsyncSession = Depends(db_handler.get_db)
):
    return await TagCRUD(session).update(tag_id, tag, False)


@router.patch(
    "/{tag_id}", response_model=TagCreate, status_code=status.HTTP_202_ACCEPTED
)
async def replace(
    tag_id: UUID, tag: TagCreate, session: AsyncSession = Depends(db_handler.get_db)
):
    return await TagCRUD(session).update(tag_id, tag, True)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(tag_id: UUID, session: AsyncSession = Depends(db_handler.get_db)):
    return await TagCRUD(session).remove(tag_id)
