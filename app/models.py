from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db import db


class TimestampModel(db.Model):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True,
    )
