from datetime import datetime

swd = {
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
}
