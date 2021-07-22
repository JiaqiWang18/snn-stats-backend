from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate

import os

app = Flask(__name__)
cors = CORS(app)

DATABASE_URL = os.environ.get("SNN_RDS_URL")
print(DATABASE_URL)
DATABASE_PASS = os.environ.get("SNN_RDS_PASS")
DATABASE_USER = 'admin'
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_URL}/covid_data"

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from server import routes
from server import models