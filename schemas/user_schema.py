from marshmallow import fields, Schema, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3))
    name = fields.String(required=True)
    nim = fields.String(required=True)
    jurusan = fields.String(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf(['admin', 'user']))