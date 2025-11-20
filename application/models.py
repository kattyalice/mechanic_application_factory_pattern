from application.extensions import db
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List



# MODELS
class Base(DeclarativeBase):
    pass




service_mechanics = db.Table(
'service_mechanics',
Base.metadata,
db.Column('ticket_id', db.ForeignKey('service_tickets.id'), primary_key=True),
db.Column('mechanic_id', db.ForeignKey('mechanics.id'), primary_key=True)
)


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(50))

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(50))
    salary: Mapped[float] = mapped_column(db.Float)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_mechanics,
        back_populates="mechanics"
    )


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(255))
    service_date: Mapped[str] = mapped_column(db.String(255))
    service_desc: Mapped[str] = mapped_column(db.String(255))

    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    customer: Mapped["Customer"] = db.relationship(back_populates="service_tickets")

    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        secondary=service_mechanics,
        back_populates="tickets"
    )
    
