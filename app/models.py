from app.src.database import Base

from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TIMESTAMP


class ObjectsHistory(Base):
    __tablename__ = 'prozorro_sale_objects_history'

    id = Column(Integer, primary_key=True)
    _id = Column(String(255))
    registry_object_id = Column(String(255))
    date_published = Column(TIMESTAMP)
    date_modified = Column(TIMESTAMP)
    object = Column(JSONB)

    __table_args__ = (
        Index(
            'prozorro_sale_objects_history_id_date_modified_idx',
            _id, date_modified.desc()
        ),
        {'schema': 'src'},
    )


class AuctionsHistory(Base):
    __tablename__ = 'prozorro_sale_auctions_history'

    id = Column(Integer, primary_key=True)
    _id = Column(String(255))
    auction_id = Column(String(255))
    date_published = Column(TIMESTAMP)
    date_modified = Column(TIMESTAMP)
    object = Column(JSONB)

    __table_args__ = (
        Index(
            'prozorro_sale_auctions_history_id_date_modified_idx',
            _id, date_modified.desc()
        ),
        {'schema': 'src'},
    )


__all__ = ['ObjectsHistory', 'AuctionsHistory']
