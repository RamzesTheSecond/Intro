from datetime import datetime
from sqlalchemy import create_engine, String, Integer, DateTime, Boolean, Float, func, select, update, delete, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
import random

# II
class Base(DeclarativeBase):
    pass

class Experiment(Base):
    __tablename__ = "experiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    #data_points: Mapped[list["DataPoint"]] = relationship(
    #    back_populates="experiment",
    #    cascade="all, delete-orphan"
    #)

class DataPoint(Base):
    __tablename__ = "data_point"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    #experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"), nullable=False)
    #experiment: Mapped["Experiment"] = relationship(back_populates="data_points")

engine = create_engine("sqlite:///experiments.db")
Base.metadata.create_all(engine)

# III.1,2
engine = create_engine("sqlite:///experiments.db")

with Session(engine) as session:
    exp1 = Experiment(title="Test1", type=1)
    exp2 = Experiment(title="Test2", type=2)

    data_points = [
        DataPoint(
            real_value=round(random.uniform(0.0, 100.0), 2),
            target_value=round(random.uniform(0.0, 100.0), 2),
            #experiment=exp1,
        )
        for _ in range(10)
    ]

session.add_all([exp1, exp2])
session.add_all(data_points)
session.commit()

# III.3
with Session(engine) as session:
    print("=== Zawartość tabeli Experiment ===")
    experiments = session.scalars(select(Experiment)).all()
    for exp in experiments:
        print(f"id={exp.id}, title='{exp.title}', type={exp.type}, finished={exp.finished}, created_at={exp.created_at}")

    print("\n=== Zawartość tabeli DataPoint ===")
    data_points = session.scalars(select(DataPoint)).all()
    for dp in data_points:
        print(f"id={dp.id}, real_value={dp.real_value}, target_value={dp.target_value}")

# III.4
result = session.execute(
    update(Experiment).values(finished=True)
)
session.commit()

# III.5
session.execute(delete(DataPoint))
session.execute(delete(Experiment))
session.commit()

#IV - zakomentowany kod

#V

