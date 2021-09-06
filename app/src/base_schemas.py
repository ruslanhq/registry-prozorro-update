from typing import List, Optional, Dict

from pydantic import BaseModel, Field


class ObjectsHistoryBase(BaseModel):
    id: str = Field(..., alias='_id')
    registry_object_id: str
    date_published: str
    date_modified: str
    object: Optional[Dict]

    class Config:
        orm_mode = True


class AuctionsHistoryBase(BaseModel):
    id: str = Field(..., alias='_id')
    auction_id: str
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


class ResponseSchemaObjects(BaseModel):
    items: List[ObjectsHistoryBase]
    meta_info: MetaInfoSchema

    class Config:
        orm_mode = True


class ResponseSchemaAuctions(BaseModel):
    items: List[AuctionsHistoryBase]
    meta_info: MetaInfoSchema

    class Config:
        orm_mode = True
