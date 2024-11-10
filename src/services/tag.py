from sqlalchemy.ext.asyncio import AsyncSession

from models import TagModel
from schemas import TagCreate
from services.crud import CRUDBase


class TagCRUD(CRUDBase[TagModel, TagCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TagModel)
