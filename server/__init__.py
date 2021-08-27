from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask_caching import Cache
import os

app = Flask(__name__)
cors = CORS(app)
DATABASE_URL = os.environ.get("SNN_RDS_URL")
DATABASE_PASS = os.environ.get("SNN_RDS_PASS")
DATABASE_USER = 'admin'
REDIS_URL = os.environ.get("REDIS_URL")
config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "RedisCache",  # Flask-Caching related configs
    "CACHE_REDIS_URL": REDIS_URL,
    'JSON_SORT_KEYS': False,
    "SQLALCHEMY_DATABASE_URI": f"mysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_URL}/covid_data"
}

app.config.from_mapping(config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
cache = Cache()
cache.init_app(app)
from server import routes
from server import models
