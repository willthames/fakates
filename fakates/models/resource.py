from fakates.models.db import get_db, next_resource_version
from datetime import datetime
import uuid
from tinydb import Query


def gvk_query(group, version, kind, namespace, resource):
    query = Query()
    result = ((query.group == group) &
              (query.version == version) &
              (query.kind == kind) &
              (query.resource == resource))
    if namespace:
        result &= (query.namespace == namespace)
    return result


def get(group, version, kind, namespace, resource):
    db = get_db()
    return db.get(gvk_query(group, version, kind, namespace, resource))


def create(group, version, kind, namespace, resource, definition):
    definition['metadata']['resourceVersion'] = str(next_resource_version())
    definition['metadata']['creationTimestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    definition['metadata']['uid'] = str(uuid.uuid4())
    params = dict(group=group, version=version, kind=kind,
                  resource=resource, definition=definition)
    if namespace:
        params['namespace'] = namespace
    db = get_db()
    db.insert(params)
    return definition


def update(group, version, kind, namespace, resource, definition):
    before = get(group, version, kind, namespace, resource)
    before['metadata'].update(definition['metadata'])
    if before != definition:
        definition['metadata']['resourceVersion'] = str(next_resource_version())
    params = dict(group=group, version=version, kind=kind,
                  resource=resource, definition=definition)
    if namespace:
        params['namespace'] = namespace
    db = get_db()
    db.update(params, gvk_query(group, version, kind, namespace, resource))
    return definition


def delete(group, version, kind, namespace, resource):
    before = get(group, version, kind, namespace, resource)
    db = get_db()
    db.remove(gvk_query(group, version, kind, namespace, resource))
    #before['status']['phase'] = 'Terminating'
    return before
