from flask import Blueprint, request, jsonify

from app.db import db
from app.user.models import User

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["POST"])
def create_user():
    """
    Create a new User record
    """
    data = request.json

    new_user = User(
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_user.id,
                "username": new_user.username,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "phone": new_user.phone,
            }
        ),
        201,
    )
