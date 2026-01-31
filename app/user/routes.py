from typing import Sequence

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db
from app.user.models import User
from app.user.schemas import user_schema
from app.utils import config_logger

# Config Logger
log = config_logger("UserRoutes")

bp = Blueprint("user", __name__, url_prefix="/user")


def create_user(data):
    """
    Create a new User record
    """
    log.info("Started user creation")
    try:
        new_user = User(
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            password=generate_password_hash(data["password"]),
        )

        db.session.add(new_user)
        db.session.commit()

        log.debug(f"User with ID {new_user.id} was created")
        log.info("Finished user creation")

        return user_schema.dump(new_user)
    except IntegrityError as e:
        log.exception(f"IntegrityError during user creation: {e}")
        db.session.rollback()

        return {"error": "Duplicate data insertion."}


@bp.route("/", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
        - User Registration
    produces:
        - application/json
    parameters:
        - name: user
          in: body
          description: User data
          required: true
          schema:
            $ref: '#/definitions/UserIn'
    responses:
        201:
           description: User created
           schema:
             $ref: '#/definitions/UserOut'
        400:
           description: Duplicate data insertion
        422:
           description: Validation error
    """
    # Get data
    json_data = request.json

    try:
        data = user_schema.load(json_data)
    except ValidationError as e:
        log.exception(f"ValidationError during user creation: {str(e.messages)}")
        return jsonify(e.messages), 422

    # Set is_active to False
    data["is_active"] = False

    # Create User
    user = create_user(data)

    if "error" in user:
        return jsonify(user), 400

    # TO DO: Send email verification

    return (
        jsonify(user),
        201,
    )


@bp.route("/login", methods=["POST"])
def login():
    """
    Login a user
    ---
    tags:
        - User Login
    produces:
        - application/json
    parameters:
        - name: user
          in: body
          description: User data
          required: true
          schema:
            $ref: '#/definitions/UserIn'
    responses:
        200:
           description: Login successful
           schema:
             $ref: '#/definitions/TokenOut'
        401:
           description: Invalid credentials
        404:
           description: User not found
           schema:
             $ref: '#/definitions/NotFound'
        422:
           description: Validation error
    """

    log.info("Started user login")

    # Get data
    json_data = request.json

    try:
        no_fields: Sequence[str] = ["username", "first_name", "last_name", "phone"]
        data = user_schema.load(json_data, partial=no_fields)
    except ValidationError as e:
        log.exception(f"ValidationError during user login: {str(e.messages)}")
        return jsonify(e.messages), 422

    # Get User
    user = db.first_or_404(db.select(User).filter_by(email=data["email"]))

    if not check_password_hash(user.password, data["password"]):
        return jsonify(error="Incorrect email or password"), 401

    token = create_access_token(identity=user.email)

    log.debug(f"User with ID {user.id} was logged in")
    log.info("Finished user login")

    return jsonify(token=token), 200
