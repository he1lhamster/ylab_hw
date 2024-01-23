import uuid
from sqlalchemy import ForeignKey, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Menu(Base):
    __tablename__ = "menu"
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    title: Mapped[str]
    description: Mapped[str]


class Submenu(Base):
    __tablename__ = "submenu"
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    title: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped["Menu"] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))


class Dish(Base):
    __tablename__ = "dish"
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    title: Mapped[str]
    description: Mapped[str]
    submenu_id: Mapped["Submenu"] = mapped_column(ForeignKey("submenu.id", ondelete="CASCADE"))
    price: Mapped[str] = mapped_column(Numeric(precision=6, scale=2))
