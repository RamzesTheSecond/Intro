# V.py
from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, Boolean, Float, ForeignKey, func, MetaData, Table, Column
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)

class Experiment(Base):
    __tablename__ = "experiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")

    data_points: Mapped[list["DataPoint"]] = relationship(
        back_populates="experiment",
        cascade="all, delete-orphan"
    )

class DataPoint(Base):
    __tablename__ = "data_point"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"), nullable=False)
    experiment: Mapped["Experiment"] = relationship(back_populates="data_points")

subject_experiment = Table(
    "subject_experiment",
    Base.metadata,
    Column("subject_id", ForeignKey("subject.id"), primary_key=True),
    Column("experiment_id", ForeignKey("experiment.id"), primary_key=True),
)
class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    gdpr_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")

    experiments: Mapped[list["Experiment"]] = relationship(
        secondary=subject_experiment,
        back_populates="subjects",
    )

# po definicji Experiment dopisz relację zwrotną:
Experiment.subjects = relationship(
    "Subject",
    secondary=subject_experiment,
    back_populates="experiments",
)