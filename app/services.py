from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.base_services import BaseManager
from app.src.http_requests import MakeRequest
from app.models import ObjectsHistory


class ObjectHistoryManager(BaseManager):
    def __init__(self, url):
        self.url = url

    async def create(self, db: AsyncSession, date_modified: str):
        last_page = self.get_last_page(self.url, date_modified)
        for page in range(1, last_page + 1):
            uri = self.url + date_modified + "?limit=100&page=" + str(page)
            try:
                request = MakeRequest(uri=uri)
                objects = await request.do_request()
                for num in range(len(objects)):
                    new_object = ObjectsHistory()
                    instance = await self.get_object(
                        db=db, _id=objects[num]['_id']
                    )
                    if instance:
                        continue
                    else:
                        new_object._id = objects[num]['_id']
                        new_object.registry_object_id = objects[num][
                            'registryObjectId'
                        ]
                        new_object.date_published = objects[num][
                            'datePublished'
                        ]
                        new_object.date_modified = objects[num]['dateModified']
                        new_object.object = objects[num]
                        db.add(new_object)
            except Exception as exc:
                print(exc)

        return status.HTTP_200_OK
