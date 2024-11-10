from uuid import UUID

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import AuthorCreate
from services import AuthorCRUD

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    author: AuthorCreate, session: AsyncSession = Depends(db_handler.get_db)
):
    return await AuthorCRUD(session).create(author)


@router.get("/", response_model=list[AuthorCreate])
async def get_all(session: AsyncSession = Depends(db_handler.get_db)):
    return await AuthorCRUD(session).get_all()


@router.get("/{author_id}", response_model=AuthorCreate)
async def get_one(author_id: UUID, session: AsyncSession = Depends(db_handler.get_db)):
    return await AuthorCRUD(session).get_one(author_id)


@router.put(
    "/{author_id}", response_model=AuthorCreate, status_code=status.HTTP_202_ACCEPTED
)
async def update(
    author_id: UUID,
    author: AuthorCreate,
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await AuthorCRUD(session).update(author_id, author, False)


@router.patch(
    "/{author_id}", response_model=AuthorCreate, status_code=status.HTTP_202_ACCEPTED
)
async def replace(
    author_id: UUID,
    author: AuthorCreate,
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await AuthorCRUD(session).update(author_id, author, True)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(author_id: UUID, session: AsyncSession = Depends(db_handler.get_db)):
    return await AuthorCRUD(session).remove(author_id)
