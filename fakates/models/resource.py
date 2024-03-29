from fakates.models.db import get_db, next_resource_version
from fakates.helpers import dict_merge
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
    table = db.table('resources')
    record =  table.get(gvk_query(group, version, kind, namespace, resource))
    if record:
        return record['definition']
    return None


def create(group, version, kind, namespace, resource, definition):
    definition['metadata']['resourceVersion'] = str(next_resource_version())
    definition['metadata']['creationTimestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    definition['metadata']['uid'] = str(uuid.uuid4())
    params = dict(group=group, version=version, kind=kind,
                  resource=resource, definition=definition)
    if namespace:
        params['namespace'] = namespace
    db = get_db()
    table = db.table('resources')
    table.insert(params)
    return definition


def replace(group, version, kind, namespace, resource, definition):
    before = get(group, version, kind, namespace, resource)
    before['metadata'].update(definition['metadata'])
    if before != definition:
        definition['metadata']['resourceVersion'] = str(next_resource_version())
    params = dict(group=group, version=version, kind=kind,
                  resource=resource, definition=definition)
    if namespace:
        params['namespace'] = namespace
    db = get_db()
    table = db.table('resources')
    table.update(params, gvk_query(group, version, kind, namespace, resource))
    return definition


def patch(group, version, kind, namespace, resource, definition):
    before = get(group, version, kind, namespace, resource)
    definition = dict_merge(before, definition, remove_nulls=True)
    return replace(group, version, kind, namespace, resource, definition)


def delete(group, version, kind, namespace, resource):
    before = get(group, version, kind, namespace, resource)
    db = get_db()
    table = db.table('resources')
    table.remove(gvk_query(group, version, kind, namespace, resource))
    # before['status']['phase'] = 'Terminating'
    if kind == 'namespaces':
        query = Query()
        cascade = table.search(query.namespace == namespace)
        for item in cascade:
            # we could delete directly here but delete will later modify
            # the watch record
            delete(cascade['group'], cascade['version'], "%ss" % cascade['kind'].lower(), namespace, cascade['resource'])
    return before
