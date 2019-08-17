from flask import Blueprint, jsonify, make_response, render_template

apis_bp = Blueprint('apis_bp', __name__, template_folder='apis')


@apis_bp.route('/apis')
def apilist():
    response = make_response(render_template('apis.json'))
    response.headers['Content-Type'] = 'application/json'
    return response


@apis_bp.route('/apis/<group>/<version>')
def apishow(group, version):
    response = make_response(render_template('%s/%s.json' % (group, version)))
    response.headers['Content-Type'] = 'application/json'
    return response


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
