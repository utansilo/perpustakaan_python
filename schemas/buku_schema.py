from marshmallow import fields, Schema, validate

class BukuSchema(Schema):
    id = fields.Int(dump_only=True)
    judul = fields.String(required=True, validate=validate.Length(min=3))
    penulis = fields.String(required=True, validate=validate.Length(min=6))
    tahun = fields.Integer(required=True)
