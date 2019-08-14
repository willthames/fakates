from flask import Flask, g
from fakates.cli import create_cli
from fakates.views.version import version_bp
from fakates.views.resource import resource_bp
from fakates.views.apis import apis_bp
from fakates.views.list import list_bp
import tinydb
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


def create_app():
    app = Flask(__name__)
    app.register_blueprint(version_bp)
    app.register_blueprint(resource_bp)
    app.register_blueprint(apis_bp)
    app.register_blueprint(list_bp)

    @app.teardown_appcontext
    def teardown_db(ex):
        db = g.pop('db', None)

        if db is not None:
            db.close()

    return app


if __name__ == '__main__':
    cli = create_cli()
    app = create_app()
    app.config['database'] = cli.database
    app.run(host=cli.host, port=cli.port)
