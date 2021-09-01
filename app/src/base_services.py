import datetime
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.src.database import Base
from app.src.http_requests import MakeRequest

# custom type for SQLAlchemy model
ModelType = TypeVar("ModelType", bound=Base)


class BaseManager:

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
            self, start_date, yesterday_date, db, model, prepare_url
    ):
        while start_date.strftime("%Y-%m-%d") !=\
                yesterday_date.strftime("%Y-%m-%d"):
            start_date += datetime.timedelta(days=1)
            url = prepare_url(start_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
            await self.update_or_create(db=db, uri=url, model=model)
