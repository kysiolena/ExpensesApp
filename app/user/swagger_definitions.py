from datetime import datetime

swd = {
    "UserIn": {
        "type": "object",
        "discriminator": "userInType",
        "properties": {
            "username": {"type": "string"},
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "password": {"type": "string"},
        },
        "example": {
            "username": "hello_world",
            "first_name": "Hello",
            "last_name": "World",
            "email": "hello@world.com",
            "phone": "+38 099 999 99 99",
            "password": "strong_password",
        },
    },
    "UserOut": {
        "allOf": [
            {"$ref": "#/definitions/UserIn"},
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
    "TokenOut": {
        "type": "object",
        "discriminator": "tokenOutType",
        "properties": {
            "token": {"type": "string"},
        },
    },
    "Unauthorized": {
        "type": "object",
        "discriminator": "unauthorizedType",
        "properties": {
            "error": {"type": "string"},
        },
        "example": {
            "error": "You have not access",
        },
    },
}
