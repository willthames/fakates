from flask import Blueprint, request, make_response, jsonify
from fakates.models.list import get

list_bp = Blueprint('list_bp', __name__)


def handle_request(group, version, namespace, kind):
    existing = get(group, version, namespace, kind, request.path)
    return jsonify(existing)


@list_bp.route('/api/v1/<kind>', methods=['GET'])
def core_cluster_resources(kind):
    return handle_request('core', 'v1', None, kind)


@list_bp.route('/api/v1/namespaces/<namespace>/<kind>', methods=['GET'])
def core_namespaced_resources(namespace, kind):
    return handle_request('core', 'v1', namespace, kind)


@list_bp.route('/apis/<group>/<version>/<kind>', methods=['GET'])
def group_cluster_resources(group, version, kind):
    return handle_request(group, version, None, kind)


@list_bp.route('/api/<group>/<version>/namespaces/<namespace>/<kind>', methods=['GET'])
def group_namespaced_resources(group, version, namespace, kind):
    return handle_request(group, version, namespace, kind)