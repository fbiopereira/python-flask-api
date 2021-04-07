import json
from bson.objectid import ObjectId
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            a = o.strftime('%Y-%m-%dT%H:%M:%SZ')
            return a
        return json.JSONEncoder.default(self, o)
