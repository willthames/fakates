from fakates.models.db import get_db, next_resource_version
from tinydb import Query


def gvk_query(group, version, kind, namespace):
    query = Query()
    result = ((query.group == group) &
              (query.version == version) &
              (query.kind == kind))
    if namespace:
        result &= (query.namespace == namespace)
    return result


def get(group, version, namespace, kind, link):
    db = get_db()
    results = db.search(gvk_query(group, version, kind, namespace))
    return {
        "kind": "%sList" % kind.capitalize()[:-1],
        "apiVersion": "v1",
        "metadata": {
            "selfLink": link,
            "resourceVersion": next_resource_version()
        },
        "items": results
    }