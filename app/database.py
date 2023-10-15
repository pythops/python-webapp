from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Database:
    def __init__(self):
        self._session: AsyncSession | None = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self, uri):
        engine = create_async_engine(uri, future=True)
        self._session = async_sessionmaker(engine)()


db = Database()
