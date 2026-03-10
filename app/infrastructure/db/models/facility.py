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


class CleanRooms(Base):
    __tablename__ = "clean_rooms"
    __table_args__ = (
        CheckConstraint(
            "room_type::text = ANY (ARRAY['processing'::character varying, 'packaging'::character varying]::text[])",
            name="clean_rooms_room_type_check",
        ),
        CheckConstraint(
            "serial_number >= 1 AND serial_number <= 10",
            name="clean_rooms_serial_number_check",
        ),
        PrimaryKeyConstraint("room_id", name="clean_rooms_pkey"),
        UniqueConstraint("serial_number", name="clean_rooms_serial_number_key"),
    )

    room_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    serial_number: Mapped[Optional[int]] = mapped_column(Integer)
    room_type: Mapped[Optional[str]] = mapped_column(
        String(20), server_default=text("'processing'::character varying")
    )
    status: Mapped[Optional[str]] = mapped_column(
        Enum(
            "available",
            "sterilizing",
            "in_use",
            "maintenance",
            "sterilized",
            name="room_status_enum",
        ),
        server_default=text("'available'::room_status_enum"),
    )
    max_technicians: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text("4")
    )
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    machines: Mapped[list["Machines"]] = relationship(
        "Machines", back_populates="machine_room"
    )
    materials: Mapped[list["Materials"]] = relationship(
        "Materials", back_populates="materials_room"
    )
    room_sessions: Mapped[list["RoomSessions"]] = relationship(
        "RoomSessions", back_populates="room"
    )
    tracking_logs: Mapped[list["TrackingLogs"]] = relationship(
        "TrackingLogs", back_populates="room"
    )


class Shifts(Base):
    __tablename__ = "shifts"
    __table_args__ = (PrimaryKeyConstraint("shift_id", name="shifts_pkey"),)

    shift_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    room_sessions: Mapped[list["RoomSessions"]] = relationship(
        "RoomSessions", back_populates="shift"
    )


class RoomSessions(Base):
    __tablename__ = "room_sessions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["donor_id"],
            ["donors.donor_id"],
            ondelete="SET NULL",
            name="room_sessions_donor_id_fkey",
        ),
        ForeignKeyConstraint(
            ["room_id"],
            ["clean_rooms.room_id"],
            ondelete="SET NULL",
            name="room_sessions_room_id_fkey",
        ),
        ForeignKeyConstraint(
            ["shift_id"],
            ["shifts.shift_id"],
            ondelete="SET NULL",
            name="room_sessions_shift_id_fkey",
        ),
        PrimaryKeyConstraint("session_id", name="room_sessions_pkey"),
        Index(
            "idx_one_active_session_per_room",
            "room_id",
            unique=True,
            postgresql_where=text("status = 'active'::session_status_enum"),
        ),
        Index("idx_sessions_donor", "donor_id"),
        Index("idx_sessions_room", "room_id"),
        Index("idx_sessions_status", "status"),
    )

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[Optional[int]] = mapped_column(Integer)
    shift_id: Mapped[Optional[int]] = mapped_column(Integer)
    donor_id: Mapped[Optional[int]] = mapped_column(Integer)
    queue_position: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text("0")
    )
    status: Mapped[Optional[str]] = mapped_column(
        Enum("planned", "active", "completed", "cleaning", name="session_status_enum"),
        server_default=text("'planned'::session_status_enum"),
    )
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cleaned_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    technician_count: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text("0")
    )
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    donor: Mapped[Optional["Donors"]] = relationship(
        "Donors", back_populates="room_sessions"
    )
    room: Mapped[Optional["CleanRooms"]] = relationship(
        "CleanRooms", back_populates="room_sessions"
    )
    shift: Mapped[Optional["Shifts"]] = relationship(
        "Shifts", back_populates="room_sessions"
    )
    session_technicians: Mapped[list["SessionTechnicians"]] = relationship(
        "SessionTechnicians", back_populates="session"
    )
    processes: Mapped[list["Processes"]] = relationship(
        "Processes", back_populates="session"
    )
