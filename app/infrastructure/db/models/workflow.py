import datetime, decimal
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
    Text,
    Boolean,
    Numeric,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base_class import Base, TimestampMixin


class Workflows(Base):
    __tablename__ = "workflows"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            ["tissue_categories.category_id"],
            ondelete="SET NULL",
            name="workflows_category_id_fkey",
        ),
        PrimaryKeyConstraint("workflow_id", name="workflows_pkey"),
        UniqueConstraint(
            "category_id", "name", "version", name="unique_workflow_version"
        ),
        Index("idx_workflows_template", "template_json"),
    )

    workflow_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer)
    type: Mapped[Optional[str]] = mapped_column(
        String(20), server_default=text("'production'::character varying")
    )
    name: Mapped[Optional[str]] = mapped_column(String(100))
    template_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    version: Mapped[Optional[str]] = mapped_column(String(10))
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    category: Mapped[Optional["TissueCategories"]] = relationship(
        "TissueCategories", back_populates="workflows"
    )
    processes: Mapped[list["Processes"]] = relationship(
        "Processes", back_populates="workflow"
    )


class WorkflowSteps(Base):
    __tablename__ = "workflow_steps"
    __table_args__ = (
        ForeignKeyConstraint(
            ["process_id"],
            ["processes.process_id"],
            ondelete="CASCADE",
            name="workflow_steps_process_id_fkey",
        ),
        PrimaryKeyConstraint("step_id", name="workflow_steps_pkey"),
        UniqueConstraint("process_id", "step_num", name="unique_process_step"),
        Index("idx_wf_steps_process_step", "process_id", "step_num"),
    )

    step_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[Optional[int]] = mapped_column(Integer)
    step_num: Mapped[Optional[int]] = mapped_column(Integer)
    initials: Mapped[Optional[str]] = mapped_column(String(10))
    verified_by_initials: Mapped[Optional[str]] = mapped_column(String(10))
    spin_program: Mapped[Optional[str]] = mapped_column(String(20))
    spin_count: Mapped[Optional[int]] = mapped_column(Integer)
    actual_duration: Mapped[Optional[str]] = mapped_column(String(20))
    temp_start: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    temp_stop: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    temp_compliant: Mapped[Optional[bool]] = mapped_column(Boolean)
    na_performed: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("false")
    )
    deviation_notes: Mapped[Optional[str]] = mapped_column(Text)
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    step_data: Mapped[Optional[dict]] = mapped_column(
        JSONB, server_default=text("'{}'::jsonb")
    )
    device_id: Mapped[Optional[str]] = mapped_column(String(50))
    client_timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    process: Mapped[Optional["Processes"]] = relationship(
        "Processes", back_populates="workflow_steps"
    )
