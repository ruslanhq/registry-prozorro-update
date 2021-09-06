import datetime

from typing import TypeVar, ClassVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.src.database import Base
from app.src.http_requests import MakeRequest
from app.src.paginations import PagePagination

# custom type for SQLAlchemy model
ModelType = TypeVar("ModelType", bound=Base)


class BaseManager:
    schema = None
    use_pagination = False
    pagination_class = PagePagination

    @staticmethod
    async def result(db: AsyncSession, queryset, to_instance=False):
        result = await db.stream(queryset)
        _scalar = result.scalars()
        return await (_scalar.first() if to_instance else _scalar.all())

    @staticmethod
    def _get_last_page(url: str, date_modified: str) -> int:
        """get the number of existing pages"""
        uri = url + date_modified + "?limit=100&page=10000"
        request = MakeRequest(uri=uri)
        response = request.do_sync_request()
        return response['last_page']

    @staticmethod
    async def save_object(
            db: AsyncSession, model: ModelType, objects: list, index: int
    ):
        new_object = model()
        new_object._id = objects[index]['_id']
        if model.__tablename__ == 'prozorro_sale_objects_history':
            new_object.registry_object_id = objects[index][
                'registryObjectId'
            ]
        else:
            new_object.auction_id = objects[index][
                'auctionId'
            ]
        new_object.date_published = objects[index][
            'datePublished'
        ]
        new_object.date_modified = objects[index][
            'dateModified'
        ]
        new_object.object = objects[index]
        db.add(new_object)
        await db.commit()
        return objects

    async def get_object(
            self, db: AsyncSession, model: ModelType,
            _id: str, date_modified: str
    ):
        queryset = (
            select(model)
            .filter(model._id == _id, model.date_modified == date_modified)
        )
        return await self.result(db=db, queryset=queryset, to_instance=True)

    async def count_rows(self, db: AsyncSession, model: ModelType):
        """Check if records exist"""
        from sqlalchemy import func, select
        queryset = (select([func.count()]).select_from(model))
        return await self.result(db=db, queryset=queryset, to_instance=True)

    async def get_last_date(self, db: AsyncSession, model: ModelType):
        queryset = (
            select(model.date_modified)
            .order_by(model.date_modified.desc())
            .limit(1)
        )
        return await self.result(db=db, queryset=queryset, to_instance=True)

    async def check_and_create_object(
            self, db: AsyncSession, model: ModelType,
            objects: list, index: int, _id: str, date_modified: str
    ):
        instance = await self.get_object(
            db=db, model=model, _id=_id, date_modified=date_modified
        )
        if not instance:
            await self.save_object(
                db=db, model=model,
                objects=objects, index=index
            )
        return instance

    async def update_or_create(
            self, db: AsyncSession, uri: str, model: ModelType
    ):
        objects = await MakeRequest(uri=uri).do_request()
        for index in range(len(objects)):
            await self.check_and_create_object(
                db=db, model=model, objects=objects,
                index=index, _id=objects[index]['_id'],
                date_modified=objects[index]['dateModified']
            )

    async def update_or_create_auctions(
            self, db, model, prepare_url, newest_date=None, start_date=None
    ):
        yesterday_date = datetime.datetime.today() - datetime.timedelta(1)
        if start_date:
            last_date = datetime.datetime.strptime(
                start_date, '%Y-%m-%dT%H:%M:%SZ'
            )
            url = prepare_url(start_date)
        else:
            last_date = datetime.datetime.strptime(
                newest_date, '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            url = prepare_url(newest_date)

        while last_date < yesterday_date:
            await self.update_or_create(db=db, uri=url, model=model)
            last_date_str = await self.get_last_date(db=db, model=model)
            url = prepare_url(last_date_str)
            last_date = datetime.datetime.strptime(
                last_date_str, '%Y-%m-%dT%H:%M:%S.%fZ'
            )

    async def get_list(
            self, db: AsyncSession, queryset: ClassVar,
            page_size: int, page: int = 1
    ):
        if self.use_pagination:
            total = len(await self.result(db, queryset))
            queryset = self.pagination_class.get_query(
                query=queryset, page=page, page_size=page_size
            )
            items = await self.result(db, queryset=queryset)
            return self.pagination_class(
                items, page, page_size, total, self.schema
            )
        else:
            return await self.result(db=db, queryset=queryset)


class BaseAPIManager(BaseManager):
    use_pagination = True
    pagination_class = PagePagination

    def __init__(self, model):
        self.model = model

    async def get_versions_object_by_id(
            self, db: AsyncSession, _id: str, page: int, page_size: int
    ):
        queryset = (
            select(self.model)
            .filter(self.model._id == _id)
        )
        return await self.get_list(
            db=db, queryset=queryset, page=page, page_size=page_size
        )

    async def get_object_by_id(self, db: AsyncSession, _id: str):
        queryset = (
            select(self.model)
            .filter(self.model._id == _id)
            .order_by(self.model.date_modified.desc())
            .limit(1)
        )
        return await self.result(db=db, queryset=queryset, to_instance=True)

    async def get_list_objects(
            self, db: AsyncSession, date_modified: str,
            page: int, page_size: int
    ):
        queryset = (
            select(self.model)
            .filter(self.model.date_modified >= date_modified)
        )
        return await self.get_list(
            db=db, queryset=queryset, page=page, page_size=page_size
        )
