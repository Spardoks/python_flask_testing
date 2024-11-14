import os

import pydantic
from dotenv import dotenv_values, load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class AdModel(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String(255), index=True, nullable=False)


class ValidatatorAdModel(pydantic.BaseModel):
    title: str
    description: str
    owner: str

    @pydantic.validator("title")
    def min_max_length(cls, value: str):
        if 1 > len(value) > 50:
            raise ValueError("Title should be from 1 to 50 characters")
        return value


Config = dotenv_values(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env")
)
load_dotenv()

POSTGRES_USER = Config["POSTGRES_USER"]
POSTGRES_PASSWORD = Config["POSTGRES_PASSWORD"]
POSTGRES_DB = Config["POSTGRES_DB"]
PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
