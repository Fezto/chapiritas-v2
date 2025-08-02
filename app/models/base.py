from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class BaseModelSimple(SQLModel):
    """Base model para tablas SIN deleted_at"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": sa.func.now(), "server_default": sa.func.now()},
    )


class BaseModel(BaseModelSimple):
    """Base model para tablas CON deleted_at (soft delete)"""
    deleted_at: datetime | None = Field(default=None, nullable=True)