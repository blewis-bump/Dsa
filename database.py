import os
from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analyses.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    algo: Mapped[str] = mapped_column(String(100), index=True)
    step: Mapped[int] = mapped_column(Integer)
    n_min: Mapped[int] = mapped_column(Integer)
    n_max: Mapped[int] = mapped_column(Integer)
    input_sizes: Mapped[list] = mapped_column(JSON)
    times: Mapped[list] = mapped_column(JSON)
    snapshot_path: Mapped[str] = mapped_column(String(500))
    image_base64: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


def init_db():
    Base.metadata.create_all(engine)
