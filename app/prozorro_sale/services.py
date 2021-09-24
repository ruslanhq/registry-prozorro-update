from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.base_services import BaseManager
from app.src.http_requests import MakeRequest
from app.src.logger import logger, logger_info
from app.src.settings import settings
from app.prozorro_sale.models import ObjectsHistory, AuctionsHistory


class ObjectHistoryManager(BaseManager):
    url = settings.OBJECTS_API_URL
    model = ObjectsHistory

    def _prepare_url(self, date_modified: str, page: int) -> str:
        return self.url + f"{date_modified}?limit=100&page={page}"

    async def create(self, db: AsyncSession, date_modified: str):
        exist_row = await self.count_rows(db=db, model=self.model)
        if not exist_row:
            try:
                last_page = self._get_last_page(
                    url=self.url, date_modified=date_modified
                )
                for page in range(1, last_page + 1):
                    uri = self._prepare_url(date_modified, page)
                    logger_info.info(
                        f"""Request to prozzoro_sale for get all objects_history
                         from date_modified - {date_modified}, page - {page}"""
                    )
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
        try:
            last_date = last_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            last_page = self._get_last_page(
                url=self.url, date_modified=last_date
            )
            for page in range(1, last_page + 1):
                uri = self._prepare_url(last_date, page)
                logger_info.info(
                    f"""Request to prozzoro_sale for get new objects_history
                     from date_modified - {last_date}, page - {page}"""
                )
                await self.update_or_create(db=db, uri=uri, model=self.model)
        except Exception as exc:
            print(exc)
            logger.exception(exc)
            return status.HTTP_408_REQUEST_TIMEOUT
        return status.HTTP_200_OK


class AuctionsHistoryManager(BaseManager):
    url = settings.AUCTIONS_API_URL
    model = AuctionsHistory

    def _prepare_url(self, date_modified: str) -> str:
        return self.url + f"{date_modified}?limit=100"

    async def create(self, db: AsyncSession, date_modified: str):
        exist_row = await self.count_rows(db=db, model=self.model)
        if not exist_row:
            try:
                logger_info.info(
                    f"""Request to prozzoro_sale for get all auctions_history
                     from date_modified - {date_modified}"""
                )
                await self.update_or_create_auctions(
                    start_date=date_modified, db=db,
                    model=self.model, prepare_url=self._prepare_url
                )
                return status.HTTP_201_CREATED
            except Exception as exc:
                print(exc)
                logger.exception(exc)
                return status.HTTP_408_REQUEST_TIMEOUT
        else:
            last_date = await self.get_last_date(db=db, model=self.model)
            try:
                logger_info.info(
                    f"""Request to prozzoro_sale for get new auctions_history
                     from date_modified - {last_date}"""
                )
                await self.update_or_create_auctions(
                    db=db, newest_date=last_date,
                    model=self.model, prepare_url=self._prepare_url
                )
            except Exception as exc:
                print(exc)
                logger.exception(exc)
                return status.HTTP_408_REQUEST_TIMEOUT
        return status.HTTP_200_OK
