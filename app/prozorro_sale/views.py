import datetime

from typing import Optional

from fastapi import Depends, HTTPException, Query

from starlette.status import HTTP_404_NOT_FOUND

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.prozorro_sale.services import (
    ObjectHistoryManager, AuctionsHistoryManager
)
from app.prozorro_sale.models import ObjectsHistory, AuctionsHistory
from app.src.base_services import BaseAPIManager
from app.src.settings import settings
from app.src.database import get_db_instance
from app.src.base_schemas import (
    ResponseSchemaObjects, ObjectsHistoryBase,
    AuctionsHistoryBase, ResponseSchemaAuctions
)

router = InferringRouter(tags=['api'])


@cbv(router)
class ObjectsViewSet(ObjectHistoryManager):
    use_pagination = True
    schema = ObjectsHistoryBase
    api_class = BaseAPIManager
    model = ObjectsHistory
    session: AsyncSession = Depends(get_db_instance)

    @router.get("/get_objects_history")
    async def get_and_save_objects(
            self, date_modified: Optional[str] = settings.DATE_MODIFIED
    ):
        return await self.create(db=self.session, date_modified=date_modified)

    @router.get('/versions/object/{_id}', response_model=ResponseSchemaObjects)
    async def versions_object_by_id(
            self, _id: str,
            page: int = Query(1, gt=0),
            page_size: int = Query(1, gt=0)
    ):
        items = await self.api_class(self.model).get_versions_object_by_id(
            db=self.session, _id=_id, page=page, page_size=page_size
        )
        if not items:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return ResponseSchemaObjects.from_orm(items)

    @router.get('/object/{_id}', response_model=ObjectsHistoryBase)
    async def object_by_id(self, _id: str):
        item = await self.api_class(self.model).get_object_by_id(
            db=self.session, _id=_id
        )
        if not item:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return self.schema.from_orm(item)

    @router.get('/objects/', response_model=ResponseSchemaObjects)
    async def list_objects(
            self, date_modified: datetime.datetime = settings.DATE_MODIFIED,
            page: int = Query(1, gt=0),
            page_size: int = Query(1, gt=0)
    ):
        items = await self.api_class(self.model).get_list_objects(
            db=self.session, date_modified=date_modified.isoformat(),
            page=page, page_size=page_size
        )
        if not items:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return ResponseSchemaObjects.from_orm(items)


@cbv(router)
class AuctionsViewSet(AuctionsHistoryManager):
    use_pagination = True
    schema = AuctionsHistoryBase
    api_class = BaseAPIManager
    model = AuctionsHistory
    session: AsyncSession = Depends(get_db_instance)

    @router.get("/get_auctions_history")
    async def get_objects(
            self, date_modified: Optional[str] = settings.DATE_MODIFIED
    ):
        return await self.create(db=self.session, date_modified=date_modified)

    @router.get(
        '/versions/auctions/{_id}', response_model=ResponseSchemaAuctions
    )
    async def versions_object_by_id(
            self, _id: str,
            page: int = Query(1, gt=0),
            page_size: int = Query(1, gt=0)
    ):
        items = await self.api_class(self.model).get_versions_object_by_id(
            db=self.session, _id=_id, page=page, page_size=page_size
        )
        if not items:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return ResponseSchemaAuctions.from_orm(items)

    @router.get('/auction/{_id}', response_model=AuctionsHistoryBase)
    async def object_by_id(self, _id: str):
        item = await self.api_class(self.model).get_object_by_id(
            db=self.session, _id=_id
        )
        if not item:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return self.schema.from_orm(item)

    @router.get('/auctions/', response_model=ResponseSchemaAuctions)
    async def list_objects(
            self, date_modified: datetime.datetime = settings.DATE_MODIFIED,
            page: int = Query(1, gt=0),
            page_size: int = Query(1, gt=0)
    ):
        items = await self.api_class(self.model).get_list_objects(
            db=self.session, date_modified=date_modified.isoformat(),
            page=page, page_size=page_size
        )
        if not items:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        return ResponseSchemaAuctions.from_orm(items)
