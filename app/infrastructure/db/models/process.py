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


class Processes(Base):
    __tablename__ = "processes"
    __table_args__ = (
        ForeignKeyConstraint(
            ["plan_id"],
            ["production_plans.plan_id"],
            ondelete="SET NULL",
            name="processes_plan_id_fkey",
        ),
        ForeignKeyConstraint(
            ["session_id"],
            ["room_sessions.session_id"],
            ondelete="SET NULL",
            name="processes_session_id_fkey",
        ),
        ForeignKeyConstraint(
            ["tissue_id"],
            ["tissues.tissue_id"],
            ondelete="SET NULL",
            name="processes_tissue_id_fkey",
        ),
        ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.workflow_id"],
            ondelete="SET NULL",
            name="processes_workflow_id_fkey",
        ),
        PrimaryKeyConstraint("process_id", name="processes_pkey"),
        Index("idx_processes_session", "session_id"),
        Index("idx_processes_status", "status"),
        Index("idx_processes_tissue", "tissue_id"),
        Index("idx_processes_workflow", "workflow_id"),
    )

    process_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[Optional[int]] = mapped_column(Integer)
    plan_id: Mapped[Optional[int]] = mapped_column(Integer)
    workflow_id: Mapped[Optional[int]] = mapped_column(Integer)
    template_snapshot: Mapped[Optional[dict]] = mapped_column(JSONB)
    tissue_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(
        Enum(
            "planned",
            "in_progress",
            "completed",
            "deviated",
            name="process_status_enum",
        ),
        server_default=text("'planned'::process_status_enum"),
    )
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    plan: Mapped[Optional["ProductionPlans"]] = relationship(
        "ProductionPlans", back_populates="processes"
    )
    session: Mapped[Optional["RoomSessions"]] = relationship(
        "RoomSessions", back_populates="processes"
    )
    tissue: Mapped[Optional["Tissues"]] = relationship(
        "Tissues", back_populates="processes"
    )
    workflow: Mapped[Optional["Workflows"]] = relationship(
        "Workflows", back_populates="processes"
    )
    process_comments: Mapped[list["ProcessComments"]] = relationship(
        "ProcessComments", back_populates="process"
    )
    verifications: Mapped[list["Verifications"]] = relationship(
        "Verifications", back_populates="process"
    )
    workflow_steps: Mapped[list["WorkflowSteps"]] = relationship(
        "WorkflowSteps", back_populates="process"
    )


class ProcessComments(Base):
    __tablename__ = "process_comments"
    __table_args__ = (
        ForeignKeyConstraint(
            ["process_id"],
            ["processes.process_id"],
            ondelete="CASCADE",
            name="process_comments_process_id_fkey",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["technicians.technician_id"],
            ondelete="SET NULL",
            name="process_comments_user_id_fkey",
        ),
        PrimaryKeyConstraint("comment_id", name="process_comments_pkey"),
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    comment_text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    process: Mapped[Optional["Processes"]] = relationship(
        "Processes", back_populates="process_comments"
    )
    user: Mapped[Optional["Technicians"]] = relationship(
        "Technicians", back_populates="process_comments"
    )
