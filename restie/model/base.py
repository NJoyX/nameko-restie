from marshmallow import SchemaOpts, fields, Schema
from restie.utils import json


class OptsOut(SchemaOpts):
    def __init__(self, meta):
        super(OptsOut, self).__init__(meta)
        self.json_module = json
        self.dateformat = 'iso8601'


class BaseRestModel(Schema):
    OPTIONS_CLASS = OptsOut


class BaseRestUUIDModel(BaseRestModel):
    uuid = fields.UUID(required=True)
