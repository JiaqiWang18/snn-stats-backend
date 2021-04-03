from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.automap import automap_base
from server import db


class OrangeCounty(db.Model, SerializerMixin):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    total_tested = db.Column(db.Integer)

class LACounty(db.Model, SerializerMixin):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)


class California(db.Model, SerializerMixin):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)


class UnitedStates(db.Model):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    recovered = db.Column(db.Integer)

# automapping the oc_cities table
Base = automap_base()
Base.prepare(db.engine, reflect=True)
OCCities = Base.classes.oc_cities