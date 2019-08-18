from fakates.models.db import get_db
from tinydb import Query

DEFAULT_VERBS = [
    "delete",
    "deletecollection",
    "get",
    "list",
    "patch",
    "create",
    "update",
    "watch"
]


def crd_to_resource(crd):
    resource = dict(
        name=crd['metadata']['name'].replace(".{}".format(crd['spec']['group']), ''),
        singularName=crd['spec']['names'].get('singular', crd['spec']['names']['kind'].lower()),
        namespaced=crd['spec']['scope'] == 'Namespaced',
        kind=crd['spec']['names']['kind'],
        verbs=crd['spec'].get('verbs', DEFAULT_VERBS)
    )
    if 'shortNames' in crd['spec']['names']:
        resource['shortNames'] = crd['spec']['names']['shortNames']
    return resource


def list_crd_apis():
    db = get_db()
    query = Query()
    table = db.table('resources')
    crds = table.search((query.group == 'apiextensions.k8s.io') &
                        (query.kind == 'customresourcedefinitions'))
    result = dict()
    for crd in crds:
        spec = crd['definition']['spec']
        if spec['group'] not in result:
            result[spec['group']] = list()
        if spec['version'] not in result[spec['group']]:
            result[spec['group']].append(spec['version'])
    return result


def get_crd_api(group, version):
    db = get_db()
    query = Query()
    table = db.table('resources')
    crds = table.search((query.group == 'apiextensions.k8s.io') &
                        (query.kind == 'customresourcedefinitions') &
                        (query.definition.spec.group == group) &
                        (query.definition.spec.version == version))
    if not crds:
        return None
    return {
        "kind": "APIResourceList",
        "apiVersion": "v1",
        "groupVersion": "%s/%s" % (group, version),
        "resources": [crd_to_resource(crd['definition']) for crd in crds]
    }
