from fakates.models.db import get_db
from fakates.models.crd import list_crd_apis, get_crd_api

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
            result[item['group']] = list()
        result[item['group']].append(item['version'])
    result.update(list_crd_apis())
    return result


def get(group, version):
    db = get_db()
    table = db.table('apis')
    result = table.get(gv_query(group, version))
    if result:
        return result['definition']
    result = get_crd_api(group, version)
    return result


def upsert(group, version, definition):
    db = get_db()
    table = db.table('apis')
    table.upsert(dict(group=group, version=version, definition=definition),
                 gv_query(group, version))
    return definition
