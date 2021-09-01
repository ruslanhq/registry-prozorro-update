from typing import Optional

from fastapi import Depends, HTTPException

from starlette.status import HTTP_404_NOT_FOUND

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.prozorro_sale.services import (
    ObjectHistoryManager, AuctionsHistoryManager
)
from app.src.settings import settings
from app.src.database import get_db_instance
from app.src.base_schemas import ObjectsHistoryBase

router = InferringRouter(tags=['api'])


@cbv(router)
class ObjectsViewSet(ObjectHistoryManager):
    schema = ObjectsHistoryBase
    session: AsyncSession = Depends(get_db_instance)

    @router.get("/get_objects_history")
    async def get_and_save_objects(
            self, date_modified: Optional[str] = settings.DATE_MODIFIED
    ):
        return await self.create(db=self.session, date_modified=date_modified)

    @router.get('/objects/{_id}')
    async def detail_objects_by_id(self, _id: str):
        item = await self.get_objects_by_id(db=self.session, _id=_id)
        if not item:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return item


@cbv(router)
class AuctionsViewSet(AuctionsHistoryManager):
    # schema = ObjectsHistoryBase
    session: AsyncSession = Depends(get_db_instance)

    @router.get("/get_auctions_history")
    async def get_objects(
            self, date_modified: Optional[str] = settings.DATE_MODIFIED
    ):
        return await self.create(db=self.session, date_modified=date_modified)
