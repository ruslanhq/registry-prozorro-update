from typing import Optional

from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.services import ObjectHistoryManager
from app.src.settings import settings
from app.src.database import get_db_instance

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
        url=settings.OBJECTS_API_URL
    ).create(db=db, date_modified=date_modified)
    return response
