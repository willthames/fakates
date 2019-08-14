from flask import Blueprint, request, make_response, jsonify
from fakates.models.resource import get, create, update, delete

resource_bp = Blueprint('resource_bp', __name__)

ALLOWED_METHODS=['GET', 'POST', 'PUT', 'DELETE']


def details_and_kind_group(group, kind, resource):
    details = {
        "name": resource,
        "kind": kind
    }
    if group != 'core':
        kind_group='{}.{}' % (kind, group)
        details['group'] = group
    else:
        kind_group = kind
    return details, kind_group


def not_found(group, version, namespace, kind, resource):
    details, kind_group = details_and_kind_group(group, kind, resource)
    response = {
          "kind": "Status",
          "apiVersion": "v1",
          "metadata": {},
          "status": "Failure",
          "message": '%s "%s" not found' % (kind, resource),
          "reason": "NotFound",
          "details": details,
          "code": 404
        }
    return make_response(jsonify(response), 404)


def already_exists(group, version, namespace, kind, resource):
    details, kind_group = details_and_kind_group(group, kind, resource)
    response = {
          "kind": "Status",
          "apiVersion": "v1",
          "metadata": {},
          "status": "Failure",
          "message": '%s "%s" already exists' % (kind, resource),
          "reason": "AlreadyExists",
          "details": details,
          "code": 409
        }
    return make_response(jsonify(response), 409)


def handle_request(group, version, namespace, kind, resource=None):
    if not resource and request.json:
        resource = request.json['metadata']['name']
    existing = get(group, version, namespace, kind, resource)
    if request.method == 'GET':
        if not existing:
            return not_found(group, version, namespace, kind, resource)
        return jsonify(existing)
    if request.method == 'POST':
        if existing:
            return already_exists(group, version, namespace, kind, resource)
        result = create(group, version, namespace, kind, resource, request.json)
        return jsonify(result)
    if request.method == 'PUT':
        result = update(group, version, namespace, kind, resource, request.json)
        return jsonify(result)
    if request.method == 'DELETE':
        if not existing:
            return not_found(group, version, namespace, kind, resource)
        result = delete(group, version, namespace, kind, resource)
        return jsonify(result)


@resource_bp.route('/api/v1/<kind>/<resource>', methods=ALLOWED_METHODS)
def core_cluster_resource(kind, resource):
    return handle_request('core', 'v1', None, kind, resource)


@resource_bp.route('/api/v1/namespaces/<namespace>/<kind>/<resource>', methods=ALLOWED_METHODS)
def core_namespaced_resource(namespace, kind, resource):
    return handle_request('core', 'v1', namespace, kind, resource)


@resource_bp.route('/apis/<group>/<version>/<kind>/<resource>', methods=ALLOWED_METHODS)
def group_cluster_resource(group, version, kind, resource):
    return handle_request(group, version, None, kind, resource)


@resource_bp.route('/api/<group>/<version>/namespaces/<namespace>/<kind>/<resource>', methods=ALLOWED_METHODS)
def group_namespaced_resource(group, version, namespace, kind, resource):
    return handle_request(group, version, namespace, kind, resource)


@resource_bp.route('/api/v1/<kind>', methods=['POST'])
def create_core_cluster_resource(kind):
    return handle_request('core', 'v1', None, kind)


@resource_bp.route('/api/v1/namespaces/<namespace>/<kind>', methods=['POST'])
def create_core_namespaced_resource(namespace, kind):
    return handle_request('core', 'v1', namespace, kind)


@resource_bp.route('/apis/<group>/<version>/<kind>', methods=['POST'])
def create_group_cluster_resource(group, version, kind):
    return handle_request(group, version, None, kind)


@resource_bp.route('/api/<group>/<version>/namespaces/<namespace>/<kind>', methods=['POST'])
def create_group_namespaced_resource(group, version, namespace, kind):
    return handle_request(group, version, namespace, kind)
