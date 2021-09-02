from typing import Optional

from fastapi import Depends, HTTPException, Query

from starlette.status import HTTP_404_NOT_FOUND

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.prozorro_sale.services import (
    ObjectHistoryManager, AuctionsHistoryManager
)
from app.src.settings import settings
from app.src.database import get_db_instance
from app.src.base_schemas import ResponseSchema, ObjectsHistoryBase

router = InferringRouter(tags=['api'])


@cbv(router)
class ObjectsViewSet(ObjectHistoryManager):
    use_pagination = True
    schema = ObjectsHistoryBase
    session: AsyncSession = Depends(get_db_instance)

    @router.get("/get_objects_history")
    async def get_and_save_objects(
            self, date_modified: Optional[str] = settings.DATE_MODIFIED
    ):
        return await self.create(db=self.session, date_modified=date_modified)

    @router.get('/objects/{_id}', response_model=ResponseSchema)
    async def detail_objects_by_id(
            self, _id: str,
            page: int = Query(1, gt=0),
            page_size: int = Query(1, gt=0)
    ):
        item = await self.get_objects_by_id(
            db=self.session, _id=_id, page=page, page_size=page_size
        )
        if not item:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return ResponseSchema.from_orm(item)


@cbv(router)
class AuctionsViewSet(AuctionsHistoryManager):
    # schema = ObjectsHistoryBase
    session: AsyncSession = Depends(get_db_instance)

    @router.get("/get_auctions_history")
    async def get_objects(
            self, date_modified: Optional[str] = settings.DATE_MODIFIED
    ):
        return await self.create(db=self.session, date_modified=date_modified)
