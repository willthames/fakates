from flask import Blueprint, request, make_response, jsonify
from fakates.models.list import get

list_bp = Blueprint('list_bp', __name__)

ALLOWED_METHODS=['GET', 'DELETE']


def handle_request(group, version, kind, namespace=None):
    if request.method == 'GET':
        existing = get(group, version, kind, namespace, request.path, request.args.get('labelSelector'))
        return jsonify(existing)


@list_bp.route('/api/v1/<kind>', methods=['GET', 'DELETE'])
def core_cluster_resources(kind):
    return handle_request('core', 'v1', kind)


@list_bp.route('/api/v1/namespaces/<namespace>/<kind>', methods=['GET', 'DELETE'])
def core_namespaced_resources(namespace, kind):
    return handle_request('core', 'v1', kind, namespace)


@list_bp.route('/apis/<group>/<version>/<kind>', methods=['GET', 'DELETE'])
def group_cluster_resources(group, version, kind):
    return handle_request(group, version, kind)


@list_bp.route('/api/<group>/<version>/namespaces/<namespace>/<kind>', methods=['GET', 'DELETE'])
def group_namespaced_resources(group, version, kind, namespace):
    return handle_request(group, version, kind, namespace)
