from typing import Optional

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.services import ObjectHistoryManager, AuctionsHistoryManager
from app.src.settings import settings
from app.src.database import get_db_instance
from app.models import ObjectsHistory, AuctionsHistory
from app.src.base_schemas import ObjectsHistoryBase, ResponseSchema

from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_objects_history")
async def get_objects(
        db: AsyncSession = Depends(get_db_instance),
        date_modified: Optional[str] = settings.DATE_MODIFIED
):
    response = await ObjectHistoryManager(
        url=settings.OBJECTS_API_URL, model=ObjectsHistory
    ).create(db=db, date_modified=date_modified)
    return response


@app.get("/get_auctions_history")
async def get_objects(
        db: AsyncSession = Depends(get_db_instance),
        date_modified: Optional[str] = settings.DATE_MODIFIED
):
    response = await AuctionsHistoryManager(
        url=settings.AUCTIONS_API_URL, model=AuctionsHistory
    ).create(db=db, date_modified=date_modified)
    return response


@app.get('/objects/{_id}', response_model=ObjectsHistoryBase)
async def detail_objects(_id: str, db: AsyncSession = Depends(get_db_instance)):
    item = await ObjectHistoryManager(
        url=settings.OBJECTS_API_URL, model=ObjectsHistory
    ).get_objects(db=db, _id=_id)
    if not item:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND
        )
    return ObjectsHistoryBase.from_orm(item)
