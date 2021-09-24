import uuid

from datetime import datetime

from app.src.database import Base

from sqlalchemy import Column, String, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.types import TIMESTAMP


class ObjectsHistory(Base):
    __tablename__ = 'prozorro_sale_objects_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _id = Column(String(255), nullable=False)
    registry_object_id = Column(String(255), nullable=False)
    date_published = Column(TIMESTAMP, nullable=False)
    date_modified = Column(TIMESTAMP, nullable=False)
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _id = Column(String(255), nullable=False)
    auction_id = Column(String(255), nullable=False)
    date_published = Column(TIMESTAMP, nullable=False)
    date_modified = Column(TIMESTAMP, nullable=False)
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


class Log(Base):
    __tablename__ = 'logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    logger = Column(String(100))  # the name of the logger.
    level = Column(String(100))  # info, debug, or error?
    trace = Column(String(9096), nullable=False)  # the full traceback printout
    msg = Column(String(4096))  # any custom log you may have included
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # the current time

    __table_args__ = ({'schema': 'src'},)

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (
            self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50]
        )


__all__ = ['ObjectsHistory', 'AuctionsHistory', 'Log']
