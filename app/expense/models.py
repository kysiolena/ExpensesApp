from sqlalchemy import String

from app.models import TimestampModel
from sqlalchemy.orm import Mapped, mapped_column


class Expense(TimestampModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float]
    description: Mapped[str] = mapped_column(String(200))

    def __repr__(self):
        return f"Expense(title={self.title}, amount={self.amount}"
