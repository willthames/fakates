from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from flask import g


DATABASE = '/tmp/db.json'


def next_resource_version():
    db = get_db()
    field = Query()
    result = db.get(field.name == 'resource_version')
    if result:
        version = result['value'] + 1
    else:
        version = 1
    db.update({'value': version}, field.name == 'resource_version')
    return version


def get_db():
    if 'db' not in g:
        g.db = TinyDB(DATABASE, storage=CachingMiddleware(JSONStorage))
    return g.db
