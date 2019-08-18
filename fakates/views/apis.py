from flask import Blueprint, jsonify, make_response, render_template
from fakates.models.apis import upsert, listapis, get

import json
import os

apis_bp = Blueprint('apis_bp', __name__, template_folder='apis')


def notfound():
    response = {
        "kind": "Status",
        "apiVersion": "v1",
        "metadata": {},
        "status": "Failure",
        "message": "the server could not find the requested resource",
        "reason": "NotFound",
        "details": {},
        "code": 404
    }
    return make_response(jsonify(response), 404)


@apis_bp.before_app_first_request
def load_apis_from_files():
    template_dir = os.path.join(apis_bp.root_path, 'apis')
    with os.scandir(template_dir) as it:
        for group in it:
            if group.is_dir():
                groupdir = os.path.join(template_dir, group)
                for versionfile in os.listdir(group):
                    # strip off '.json'
                    upsert(group.name, versionfile[:-5],
                           json.load(open(os.path.join(groupdir, versionfile))))


@apis_bp.route('/apis')
def apilist():
    response = make_response(render_template('apis.json', groups=listapis()))
    response.headers['Content-Type'] = 'application/json'
    return response


@apis_bp.route('/apis/<group>/<version>')
def apishow(group, version):
    response = get(group, version)
    if not response:
        return notfound()
    return jsonify(response)


@apis_bp.route('/api/v1')
def coreapi_v1():
    response = make_response(render_template('apiv1.json'))
    response.headers['Content-Type'] = 'application/json'
    return response


@apis_bp.route('/api')
def coreapi():
    response = make_response(render_template('api.json'))
    response.headers['Content-Type'] = 'application/json'
    return response
