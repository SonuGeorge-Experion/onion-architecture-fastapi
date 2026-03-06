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
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Boolean, Mapped, mapped_column, relationship

from app.infrastructure.db.base_class import Base, TimestampMixin


class TrackingLogs(Base):
    __tablename__ = "tracking_logs"
    __table_args__ = (
        ForeignKeyConstraint(
            ["room_id"],
            ["clean_rooms.room_id"],
            ondelete="SET NULL",
            name="tracking_logs_room_id_fkey",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["technicians.technician_id"],
            ondelete="SET NULL",
            name="tracking_logs_user_id_fkey",
        ),
        PrimaryKeyConstraint("log_id", name="tracking_logs_pkey"),
        Index("idx_tracking_entity", "entity_type", "entity_id"),
        Index("idx_tracking_timestamp", "timestamp"),
    )

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[Optional[str]] = mapped_column(
        Enum("tissue", "process", "plan", "session", name="entity_type_enum")
    )
    entity_id: Mapped[Optional[int]] = mapped_column(Integer)
    event_type: Mapped[Optional[str]] = mapped_column(
        Enum(
            "collected",
            "planned",
            "step_completed",
            "deviated",
            "movement",
            "verification",
            "session_started",
            "session_completed",
            "room_cleaned",
            name="event_type_enum",
        )
    )
    room_id: Mapped[Optional[int]] = mapped_column(Integer)
    details: Mapped[Optional[dict]] = mapped_column(JSONB)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    room: Mapped[Optional["CleanRooms"]] = relationship(
        "CleanRooms", back_populates="tracking_logs"
    )
    user: Mapped[Optional["Technicians"]] = relationship(
        "Technicians", back_populates="tracking_logs"
    )
