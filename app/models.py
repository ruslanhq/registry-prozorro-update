from app.src.database import Base

from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TIMESTAMP

from datetime import datetime


class ObjectsHistory(Base):
    __tablename__ = 'prozorro_sale_objects_history'

    id = Column(Integer, primary_key=True)
    _id = Column(String(255), nullable=False)
    registry_object_id = Column(String(255), nullable=False)
    date_published = Column(String(255), nullable=False)
    date_modified = Column(String(255), nullable=False)
    object = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        TIMESTAMP, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
    )

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
    _id = Column(String(255), nullable=False)
    auction_id = Column(String(255), nullable=False)
    date_published = Column(String(255), nullable=False)
    date_modified = Column(String(255), nullable=False)
    object = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        TIMESTAMP, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
    )

    __table_args__ = (
        Index(
            'prozorro_sale_auctions_history_id_date_modified_idx',
            _id, date_modified.desc()
        ),
        {'schema': 'src'},
    )


__all__ = ['ObjectsHistory', 'AuctionsHistory']
