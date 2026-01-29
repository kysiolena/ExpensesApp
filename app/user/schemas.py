from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    first_name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    email = fields.Str(required=True, validate=validate.Length(max=100))
    phone = fields.Str(required=True, validate=validate.Length(min=11, max=20))
    password = fields.Str(
        load_only=True, required=True, validate=validate.Length(min=8)
    )


user_schema = UserSchema()
users_schema = UserSchema(many=True)
