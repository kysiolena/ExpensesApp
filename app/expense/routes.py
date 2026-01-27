from flask import Blueprint, request, jsonify

from app.db import db
from app.expense.models import Expense

bp = Blueprint("expense", __name__, url_prefix="/expense")


@bp.route("/", methods=["POST"])
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
            $ref: '#/definitions/In'
    responses:
        201:
           description: Expense created
           schema:
              $ref: '#/definitions/Out'
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


@bp.route("/", methods=["GET"])
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
                      $ref: '#/definitions/Out'
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


@bp.route("/<int:id>", methods=["GET"])
def get_expense(id: int):
    """
    Retrieve an Expense record
    ---
    tags:
        - Expense Item
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
              $ref: '#/definitions/Out'
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


@bp.route("/<int:id>", methods=["PATCH"])
def update_expense(id: int):
    """
    Update an Expense record
    ---
    tags:
        - Expense Update
    produces:
        - application/json
    parameters:
        - name: id
          in: path
          description: Expense ID
          required: true
          type: number
        - name: expense
          in: body
          description: Data for this Expense
          required: true
          schema:
            $ref: '#/definitions/In'
    responses:
       200:
          description: Expense record updated
          schema:
             $ref: '#/definitions/Out'
       404:
          description: Expense not found
          schema:
             $ref: '#/definitions/NotFound'
    """
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


@bp.route("/<int:id>", methods=["DELETE"])
def delete_expense(id: int):
    """
    Delete an Expense record
    ---
    tags:
        - Expense Delete
    produces:
        - application/json
    parameters:
        - name: id
          in: path
          description: Expense ID
          required: true
          type: number
    responses:
        204:
           description: Expense record deleted
        404:
           description: Expense not found
           schema:
              $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)

    db.session.delete(expense)
    db.session.commit()

    return "", 204
