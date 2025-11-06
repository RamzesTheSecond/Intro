from datetime import datetime
from sqlalchemy import create_engine, String, Integer, DateTime, Boolean, Float, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Experiment(Base):
    __tablename__ = "experiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")

class DataPoint(Base):
    __tablename__ = "data_point"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)


engine = create_engine("sqlite:///experiments.db")
Base.metadata.create_all(engine)



