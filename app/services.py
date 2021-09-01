import datetime

from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.base_services import BaseManager
from app.src.http_requests import MakeRequest
from app.src.logger import logger


class ObjectHistoryManager(BaseManager):
    def __init__(self, url, model):
        self.url = url
        self.model = model

    def _prepare_url(self, date_modified: str, page: int) -> str:
        return self.url + f"{date_modified}?limit=100&page={page}"

    async def create(self, db: AsyncSession, date_modified: str):
        exist_row = await self.count_rows(db=db, model=self.model)
        if not exist_row:
            try:
                last_page = self.get_last_page(
                    url=self.url, date_modified=date_modified
                )
                for page in range(1, last_page + 1):
                    uri = self._prepare_url(date_modified, page)
                    objects = await MakeRequest(uri=uri).do_request()
                    for index in range(len(objects)):
                        await self.save_object(
                            db=db, model=self.model,
                            objects=objects, index=index
                        )
                return status.HTTP_201_CREATED
            except Exception as exc:
                print(exc)
                logger.exception(exc)
                return status.HTTP_408_REQUEST_TIMEOUT
        else:
            return await self.update(db=db)

    async def update(self, db: AsyncSession):
        last_date = await self.get_last_date(db=db, model=self.model)
        last_date = str(datetime.datetime.strptime(
            last_date, '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(microsecond=0))
        try:
            last_page = self.get_last_page(
                url=self.url, date_modified=last_date
            )
            for page in range(1, last_page + 1):
                uri = self._prepare_url(last_date, page)
                await self.update_or_create(
                    db=db, uri=uri, model=self.model, date_modified=last_date
                )
        except Exception as exc:
            print(exc)
            logger.exception(exc)
            return status.HTTP_408_REQUEST_TIMEOUT

        return status.HTTP_200_OK


class AuctionsHistoryManager(BaseManager):
    def __init__(self, url, model):
        self.url = url
        self.model = model

    def _prepare_url(self, date_modified: str) -> str:
        return self.url + f"{date_modified}?limit=100"

    async def create(self, db: AsyncSession, date_modified: str):
        exist_row = await self.count_rows(db=db, model=self.model)
        if not exist_row:
            start_date = datetime.datetime.strptime(
                date_modified, '%Y-%m-%dT%H:%M:%SZ'
            )
            yesterday_date = datetime.date.today() - datetime.timedelta(1)
            try:
                await self.update_or_create_auctions(
                    start_date=start_date, yesterday_date=yesterday_date, db=db,
                    model=self.model, prepare_url=self._prepare_url
                )
                return status.HTTP_201_CREATED
            except Exception as exc:
                print(exc)
                logger.exception(exc)
                return status.HTTP_408_REQUEST_TIMEOUT
        else:
            return await self.update(db=db)

    async def update(self, db: AsyncSession):
        last_date = await self.get_last_date(db=db, model=self.model)
        start_date = datetime.datetime.strptime(
            last_date, '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        yesterday_date = datetime.date.today() - datetime.timedelta(1)
        try:
            await self.update_or_create_auctions(
                start_date=start_date, yesterday_date=yesterday_date, db=db,
                model=self.model, prepare_url=self._prepare_url
            )
        except Exception as exc:
            print(exc)
            logger.exception(exc)
            return status.HTTP_408_REQUEST_TIMEOUT

        return status.HTTP_200_OK
