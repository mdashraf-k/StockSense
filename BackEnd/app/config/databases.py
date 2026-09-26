# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from .config import settings


# # must remove connect_args when use other databases
# # engine = create_engine(settings.database_url,
# #     pool_pre_ping=True,
# #     pool_size=5,
# #     max_overflow=10)

# # This method for sqlite databases only⬇️
# engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./stocksense.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()