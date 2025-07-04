from contextlib import contextmanager
import re
from typing import Any, Generator

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    declared_attr,
    relationship,
    sessionmaker,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.settings import settings


engine = create_engine(settings.db_uri)
session_factory = sessionmaker(engine)


@contextmanager
def get_session() -> Generator[Session, Any, Any]:
    with session_factory() as session:
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()


class BaseModel(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__camel_to_snake(cls.__name__)

    @classmethod
    def __camel_to_snake(cls, camel: str) -> str:
        snake_str = re.sub("([a-z0-9])([A-Z])", r"\1_\2", camel).lower()
        return snake_str


class Question(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answer.id", ondelete="SET NULL"))
    text: Mapped[str]


class Answer(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    video_telegram_url: Mapped[str | None]
    video_youtube_url: Mapped[str | None]
    telegram_post_url: Mapped[str | None]

    next_answer_id: Mapped[int | None] = mapped_column(ForeignKey("answer.id"))

    questions: Mapped[list[Question]] = relationship()
    next_answer: Mapped["Answer"] = relationship(remote_side=[id])
