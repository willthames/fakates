from flask import Blueprint, jsonify

version_bp = Blueprint('version_bp', __name__)


@version_bp.route('/version')
def version():
    return jsonify(dict(
        major=1,
        minor=9,
        gitVersion='v1.9.0'))
