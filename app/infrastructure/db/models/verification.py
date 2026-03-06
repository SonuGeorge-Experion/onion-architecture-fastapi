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


class Verifications(Base):
    __tablename__ = "verifications"
    __table_args__ = (
        ForeignKeyConstraint(
            ["process_id"],
            ["processes.process_id"],
            ondelete="CASCADE",
            name="verifications_process_id_fkey",
        ),
        ForeignKeyConstraint(
            ["signed_by_user_id"],
            ["technicians.technician_id"],
            ondelete="SET NULL",
            name="verifications_signed_by_user_id_fkey",
        ),
        PrimaryKeyConstraint("verif_id", name="verifications_pkey"),
    )

    verif_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[Optional[int]] = mapped_column(Integer)
    role_type: Mapped[Optional[str]] = mapped_column(String(20))
    signed_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    signature_url: Mapped[Optional[str]] = mapped_column(String(500))
    signed_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    process: Mapped[Optional["Processes"]] = relationship(
        "Processes", back_populates="verifications"
    )
    signed_by_user: Mapped[Optional["Technicians"]] = relationship(
        "Technicians", back_populates="verifications"
    )
