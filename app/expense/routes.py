from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.db import db
from app.expense.models import Expense
from app.expense.schemas import expense_schema, expenses_schema

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
            $ref: '#/definitions/ExpenseIn'
    responses:
        201:
           description: Expense created
           schema:
              $ref: '#/definitions/ExpenseOut'
    """
    json_data = request.json

    try:
        data = expense_schema.load(json_data)
    except ValidationError as e:
        return e.messages, 422

    new_expense = Expense(
        title=data["title"], amount=data["amount"], description=data["description"]
    )
    db.session.add(new_expense)
    db.session.commit()

    return (
        jsonify(expense_schema.dump(new_expense)),
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
                      $ref: '#/definitions/ExpenseOut'
    """
    expenses = Expense.query.all()

    return (
        jsonify(expenses_schema.dump(expenses)),
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
              $ref: '#/definitions/ExpenseOut'
        404:
           description: Expense not found
           schema:
               $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)

    return (
        jsonify(expense_schema.dump(expense)),
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
            $ref: '#/definitions/ExpenseIn'
    responses:
       200:
          description: Expense record updated
          schema:
             $ref: '#/definitions/ExpenseOut'
       404:
          description: Expense not found
          schema:
             $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)

    json_data = request.json

    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as e:
        return e.messages, 422

    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    expense.description = data.get("description", expense.description)

    db.session.commit()

    return (
        jsonify(expense_schema.dump(expense)),
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
