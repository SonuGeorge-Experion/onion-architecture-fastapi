import datetime
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Time,
    UniqueConstraint,
    text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base_class import Base, TimestampMixin


class Technicians(Base):
    __tablename__ = "technicians"
    __table_args__ = (
        PrimaryKeyConstraint("technician_id", name="technicians_pkey"),
        UniqueConstraint("user_id", name="technicians_user_id_key"),
    )

    technician_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    role: Mapped[Optional[str]] = mapped_column(
        Enum("technician", "supervisor", name="tech_role_enum"),
        server_default=text("'technician'::tech_role_enum"),
    )
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    tracking_logs: Mapped[list["TrackingLogs"]] = relationship(
        "TrackingLogs", back_populates="user"
    )
    session_technicians: Mapped[list["SessionTechnicians"]] = relationship(
        "SessionTechnicians", back_populates="technician"
    )
    process_comments: Mapped[list["ProcessComments"]] = relationship(
        "ProcessComments", back_populates="user"
    )
    verifications: Mapped[list["Verifications"]] = relationship(
        "Verifications", back_populates="signed_by_user"
    )


class SessionTechnicians(Base):
    __tablename__ = "session_technicians"
    __table_args__ = (
        ForeignKeyConstraint(
            ["session_id"],
            ["room_sessions.session_id"],
            ondelete="CASCADE",
            name="session_technicians_session_id_fkey",
        ),
        ForeignKeyConstraint(
            ["technician_id"],
            ["technicians.technician_id"],
            ondelete="CASCADE",
            name="session_technicians_technician_id_fkey",
        ),
        PrimaryKeyConstraint("session_tech_id", name="session_technicians_pkey"),
        UniqueConstraint("session_id", "technician_id", name="unique_session_tech"),
    )

    session_tech_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[Optional[int]] = mapped_column(Integer)
    technician_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_lead: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("false")
    )
    assigned_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    unassigned_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    session: Mapped[Optional["RoomSessions"]] = relationship(
        "RoomSessions", back_populates="session_technicians"
    )
    technician: Mapped[Optional["Technicians"]] = relationship(
        "Technicians", back_populates="session_technicians"
    )
