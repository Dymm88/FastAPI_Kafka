from sqlalchemy.ext.asyncio import AsyncSession

from models import BookModel
from schemas import BookCreate
from services.crud import CRUDBase


class BookCRUD(CRUDBase[BookModel, BookCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, BookModel)
