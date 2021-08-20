from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.src.settings import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

async_session = sessionmaker(
    autocommit=False, autoflush=False,
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


async def get_db_instance() -> Session:
    db = async_session()
    try:
        yield db
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise exc
    finally:
        await db.close()
