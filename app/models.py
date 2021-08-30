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


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    logger = Column(String(100))  # the name of the logger.
    level = Column(String(100))  # info, debug, or error?
    trace = Column(String(4096))  # the full traceback printout
    msg = Column(String(4096))  # any custom log you may have included
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # the current timestamp

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
