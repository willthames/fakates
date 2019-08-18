from flask import Blueprint, jsonify
from fakates.models.db import current_resource_version

version_bp = Blueprint('version_bp', __name__)


@version_bp.route('/version')
def version():
    return jsonify(dict(
        major=1,
        minor=9,
        gitVersion='v1.9.0',
        resourceVersion=current_resource_version()))
