from fakates.models.db import get_db, next_resource_version
from fakates.models.labels import labels_match_selectors
from tinydb import Query


def gvk_query(group, version, kind, namespace, label_selectors):
    query = Query()
    result = ((query.group == group) &
              (query.version == version) &
              (query.kind == kind))
    if namespace:
        result &= (query.namespace == namespace)
    if label_selectors:
        result &= (query.definition.metadata.labels.test(labels_match_selectors,
                                                         label_selectors))
    return result


def get(group, version, kind, namespace, link, label_selectors):
    db = get_db()
    results = [item['definition']
               for item in db.search(gvk_query(group, version, kind, namespace, label_selectors))]
    return {
        "kind": "%sList" % kind.capitalize()[:-1],
        "apiVersion": "v1",
        "metadata": {
            "selfLink": link,
            "resourceVersion": str(next_resource_version())
        },
        "items": results
    }
