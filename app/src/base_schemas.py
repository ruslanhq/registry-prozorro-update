from typing import List, Optional, Dict

from pydantic import BaseModel, Json


class ObjectsHistoryBase(BaseModel):
    _id: str
    registry_object_id: str
    date_published: str
    date_modified: str
    object: Optional[Dict]

    class Config:
        orm_mode = True


class MetaInfoSchema(BaseModel):
    page: int
    pages: int
    total: int
    has_next: bool
    has_previous: bool


class ResponseSchema(BaseModel):
    items: Optional[List]
    meta_info: MetaInfoSchema

    class Config:
        orm_mode = True
