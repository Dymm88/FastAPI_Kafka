from typing import TypeVar

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import AuthorCreate, BookCreate, TagCreate
from services.crud import CRUDBase

CreateType = TypeVar("CreateType")


class MessageHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_or_update_schema(self, table: CreateType, column: str):
        result = await self.session.execute(select(table).where(table.column == column))
        existing_entry = await result.scalar().first()
        if existing_entry:
            await CRUDBase.update(table, False)
        else:
            await CRUDBase.create(table)


async def handle_data(data, db_session: AsyncSession = Depends(db_handler.get_db)):
    headers = {
        "author": (AuthorCreate, "full_name"),
        "book": (BookCreate, "title"),
        "tag": (TagCreate, "tag_title"),
    }
    for header in headers:
        if header in data:
            await MessageHandler(db_session).create_or_update_schema(
                headers[header][0],
                headers[header][1],
            )
