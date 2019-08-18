from fakates.models.db import get_db
from tinydb import Query


def gv_query(group, version):
    query = Query()
    result = ((query.group == group) &
              (query.version == version))
    return result


def listapis():
    db = get_db()
    table = db.table('apis')
    query = Query()
    group_versions = table.search(query)
    result = dict()
    for item in group_versions:
        if item['group'] not in result:
            result[item['group']] = dict()
        result[item['group']][item['version']] = item['definition']
    return result


def get(group, version):
    db = get_db()
    table = db.table('apis')
    return table.get(gv_query(group, version))['definition']


def upsert(group, version, definition):
    db = get_db()
    table = db.table('apis')
    table.upsert(dict(group=group, version=version, definition=definition),
                 gv_query(group, version))
    return definition


def insert(group, version, definition):
    db = get_db()
    table = db.table('apis')
    table.insert(dict(group=group, version=version, definition=definition))
    return definition


def delete(group, version):
    db = get_db()
    table = db.table('apis')
    table.remove(gv_query(group, version))
    return dict()
