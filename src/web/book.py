from uuid import UUID

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import BookCreate
from services import BookCRUD

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(book: BookCreate, session: AsyncSession = Depends(db_handler.get_db)):
    return await BookCRUD(session).create(book)


@router.get("/", response_model=list[BookCreate])
async def get_all(session: AsyncSession = Depends(db_handler.get_db)):
    return await BookCRUD(session).get_all()


@router.get("/{book_id}", response_model=BookCreate)
async def get_one(book_id: UUID, session: AsyncSession = Depends(db_handler.get_db)):
    return await BookCRUD(session).get_one(book_id)


@router.put(
    "/{book_id}", response_model=BookCreate, status_code=status.HTTP_202_ACCEPTED
)
async def update(
    book_id: UUID, book: BookCreate, session: AsyncSession = Depends(db_handler.get_db)
):
    return await BookCRUD(session).update(book_id, book, False)


@router.patch(
    "/{book_id}", response_model=BookCreate, status_code=status.HTTP_202_ACCEPTED
)
async def replace(
    book_id: UUID, book: BookCreate, session: AsyncSession = Depends(db_handler.get_db)
):
    return await BookCRUD(session).update(book_id, book, True)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(book_id: UUID, session: AsyncSession = Depends(db_handler.get_db)):
    return await BookCRUD(session).remove(book_id)
