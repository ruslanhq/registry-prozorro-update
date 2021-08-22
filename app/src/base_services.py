from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import ObjectsHistory
from app.src.http_requests import MakeRequest


class BaseManager:

    @staticmethod
    async def result(db: AsyncSession, queryset, to_instance=False):
        result = await db.stream(queryset)
        _scalar = result.scalars()
        return await (_scalar.first() if to_instance else _scalar.all())

    @staticmethod
    def get_last_page(url: str, date_modified: str) -> int:
        uri = url + date_modified + "?limit=100&page=10000"
        request = MakeRequest(uri=uri)
        response = request.do_sync_request()
        return response['last_page']

    async def get_object(self, db: AsyncSession, _id: str):
        queryset = (
            select(ObjectsHistory).filter(ObjectsHistory._id == _id)
        )
        return await self.result(db=db, queryset=queryset, to_instance=True)
