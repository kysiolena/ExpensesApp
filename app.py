from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI="sqlite:///expenses.sqlite3")


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class TimestampModel(db.Model):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class Expense(TimestampModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float]
    description: Mapped[str] = mapped_column(String(200))

    def __repr__(self):
        return f"Expense(title={self.title}, amount={self.amount}"


@app.route("/")
def home():
    return jsonify(message="Hello, I'm your Expense tracking App!")


@app.route("/expense", methods=["POST"])
def create_expense():
    pass


@app.route("/expense", methods=["GET"])
def get_expenses():
    pass


@app.route("/expense/<int:id>", methods=["GET"])
def get_expense(id: int):
    pass


@app.route("/expense/<int:id>", methods=["PATCH"])
def update_expense(id: int):
    pass


@app.route("/expense/<int:id>", methods=["DELETE"])
def delete_expense(id: int):
    pass


if __name__ == "__main__":
    # Create context
    with app.app_context():
        # Create DB
        db.create_all()

    # Run Flask App
    app.run(debug=True)
