from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, Index, UniqueConstraint


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

  
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)

    username: Mapped[str] = mapped_column(String(50), default="")
    name: Mapped[str] = mapped_column(String(100), default="")
    last_name: Mapped[str] = mapped_column(String(100), default="")

    config_count: Mapped[int] = mapped_column(Integer, default=0)
    is_block: Mapped[bool] = mapped_column(Boolean, default=False)
    step: Mapped[str] = mapped_column(String(255), default="home")


    services_created: Mapped[List["Service"]] = relationship(
        back_populates="creator",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    reports_made: Mapped[List["Report"]] = relationship(
        back_populates="reporter",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="Report.user_id",
    )

    reports_received: Mapped[List["Report"]] = relationship(
        back_populates="reported",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="Report.reported_user",
    )

    likes: Mapped[List["Likes"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    details: Mapped[List["Details"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Setting(Base):
    __tablename__ = "setting"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel: Mapped[str] = mapped_column(String(100))
    support: Mapped[str] = mapped_column(String(100))


class Service(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    providers: Mapped[str] = mapped_column(String(100))
    type_product: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False)


    created_by_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        index=True,
    )


    details: Mapped[List["Details"]] = relationship(
        back_populates="service",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    creator: Mapped["User"] = relationship(
        back_populates="services_created"
    )

    likes: Mapped[List["Likes"]] = relationship(
        back_populates="service",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Report(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

 
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    )

 
    reported_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    )

    reporter: Mapped["User"] = relationship(
        back_populates="reports_made",
        foreign_keys=[user_id],
    )

    reported: Mapped["User"] = relationship(
        back_populates="reports_received",
        foreign_keys=[reported_user],
    )

    __table_args__ = (
        Index("ix_report_user_reported", "user_id", "reported_user"),
    )


class Likes(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    is_dislike: Mapped[bool] = mapped_column(Boolean, default=False)
    is_like: Mapped[bool] = mapped_column(Boolean, default=False)

    service_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("service.id", ondelete="CASCADE"),
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    )

    service: Mapped["Service"] = relationship(back_populates="likes")
    user: Mapped["User"] = relationship(back_populates="likes")

    __table_args__ = (
   
        UniqueConstraint("service_id", "user_id", name="uq_likes_service_user"),
        Index("ix_likes_service_user", "service_id", "user_id"),
    )


class Details(Base):
    __tablename__ = "details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    )

    message_id: Mapped[str] = mapped_column(String(100))
    type_message: Mapped[str] = mapped_column(String(50))


    service_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("service.id", ondelete="CASCADE"),
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="details")
    service: Mapped["Service"] = relationship(back_populates="details")