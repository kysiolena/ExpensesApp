from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint


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


@app.route("/spec")
def spec():
    swg = swagger(app)

    swg["info"]["title"] = "Expenses tracking App"
    swg["info"]["version"] = "0.0.1"
    swg["definitions"] = {
        "Hello": {
            "type": "object",
            "discriminator": "helloType",
            "properties": {
                "message": {
                    "type": "string",
                }
            },
            "example": {"message": "Hello, I'm your Expenses tracking app!"},
        },
        "ExpenseIn": {
            "type": "object",
            "discriminator": "expenseInType",
            "properties": {
                "title": {"type": "string"},
                "amount": {"type": "number"},
                "description": {"type": "string"},
            },
            "example": {
                "title": "I'm your expense!",
                "amount": 100,
                "description": "This is my expense description.",
            },
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                        "created_at": {"type": "datetime"},
                        "updated_at": {"type": "datetime"},
                    },
                    "example": {
                        "id": 0,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                    },
                },
            ]
        },
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {
                "error": {"type": "string"},
            },
            "example": {"error": "We couldn't find that"},
        },
    }

    return jsonify(swg)


# Create Swagger Blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(base_url="/docs", api_url="/spec")
# Register Swagger Blueprint
app.register_blueprint(swagger_ui_blueprint)


@app.route("/")
def home():
    """
    User greeting on the Home page
    ---
    tags:
        - Home page
    produces:
        - application/json
    responses:
        200:
           description: Greeting
           schema:
                 $ref: '#/definitions/Hello'
    """
    return jsonify(message="Hello, I'm your Expense tracking App!")


@app.route("/expense", methods=["POST"])
def create_expense():
    """
    Create a new Expense record
    ---
    tags:
        - Expense Create
    parameters:
        - name: expense
          in: body
          description: Data for this Expense
          required: true
          schema:
            $ref: '#/definitions/ExpenseIn'
    """
    data = request.json
    new_expense = Expense(
        title=data["title"], amount=data["amount"], description=data["description"]
    )
    db.session.add(new_expense)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_expense.id,
                "title": new_expense.title,
                "amount": new_expense.amount,
                "description": new_expense.description,
            }
        ),
        201,
    )


@app.route("/expense", methods=["GET"])
def get_expenses():
    """
    Retrieve all Expense records
    ---
    tags:
        - Expense List
    responses:
        200:
           description: Expense records
           schema:
                 type: array
                 items:
                      $ref: '#/definitions/ExpenseOut'
    """
    expenses = Expense.query.all()

    return (
        jsonify(
            [
                {
                    "id": expense.id,
                    "title": expense.title,
                    "amount": expense.amount,
                    "description": expense.description,
                }
                for expense in expenses
            ]
        ),
        200,
    )


@app.route("/expense/<int:id>", methods=["GET"])
def get_expense(id: int):
    """
    Retrieve an Expense record
    ---
    tags:
        - Expense
    produces:
        - application/json
    parameters:
        - name: id
          in: path
          description: Expense ID
          required: true
          type: number
    responses:
        200:
           description: Expense record
           schema:
              $ref: '#/definitions/ExpenseOut'
        404:
           description: Expense not found
           schema:
               $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)

    return (
        jsonify(
            {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
                "description": expense.description,
            }
        ),
        200,
    )


@app.route("/expense/<int:id>", methods=["PATCH"])
def update_expense(id: int):
    expense = db.get_or_404(Expense, id)

    data = request.json

    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    expense.description = data.get("description", expense.description)

    db.session.commit()

    return (
        jsonify(
            {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
                "description": expense.description,
            }
        ),
        200,
    )


@app.route("/expense/<int:id>", methods=["DELETE"])
def delete_expense(id: int):
    expense = db.get_or_404(Expense, id)

    db.session.delete(expense)
    db.session.commit()

    return "", 204


@app.errorhandler(404)
def handle_404(error):
    return jsonify(error="We couldn't find that"), 404


if __name__ == "__main__":
    # Create context
    with app.app_context():
        # Create DB
        db.create_all()

    # Run Flask App
    app.run(debug=True)
