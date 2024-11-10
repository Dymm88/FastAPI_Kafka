from sqlalchemy.ext.asyncio import AsyncSession

from models import AuthorModel
from schemas import AuthorCreate
from services.crud import CRUDBase


class AuthorCRUD(CRUDBase[AuthorModel, AuthorCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AuthorModel)
