from flask import Flask, g
from fakates.views.version import version_bp
from fakates.views.resource import resource_bp
from fakates.views.apis import apis_bp
from fakates.views.list import list_bp
import tinydb
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


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
