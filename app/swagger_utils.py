from flask import Flask
from flask_swagger import swagger

from app.expense.swagger_definitions import swd as expense_swd
from app.user.swagger_definitions import swd as user_swd


def build_swagger(app: Flask):
    swg = swagger(app)

    swg["info"]["title"] = "Expenses tracking App"
    swg["info"]["version"] = "0.0.1"
    swg["definitions"] = {
        # Base
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
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {
                "error": {"type": "string"},
            },
            "example": {"error": "We couldn't find that"},
        },
        # Expense
        **expense_swd,
        # User
        **user_swd,
    }

    return swg
