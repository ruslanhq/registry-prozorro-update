from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.src.settings import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

async_session = sessionmaker(
    autocommit=False, autoflush=False,
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

# Create sync_engine for logs
engine = create_engine(settings.DATABASE_URI_SYNC, pool_pre_ping=True)
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db_instance() -> Session:
    db = async_session()
    try:
        yield db
    except Exception as exc:
        await db.rollback()
        raise exc
    finally:
        await db.close()
