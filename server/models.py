from sqlalchemy_serializer import SerializerMixin
from server import db


class OrangeCounty(db.Model, SerializerMixin):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    total_tested = db.Column(db.Integer)
    recovered = db.Column(db.Integer)


class LACounty(db.Model, SerializerMixin):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    total_tested = db.Column(db.Integer)
    recovered = db.Column(db.Integer)


class California(db.Model, SerializerMixin):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    total_tested = db.Column(db.Integer)
    recovered = db.Column(db.Integer)


class UnitedStates(db.Model):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    total_tested = db.Column(db.Integer)


class OCCities(db.Model):
    date = db.Column(db.Date, primary_key=True)
    santa_ana = db.Column(db.Integer)
    anaheim = db.Column(db.Integer)
    garden_grove = db.Column(db.Integer)
    huntington_beach = db.Column(db.Integer)
    orange = db.Column(db.Integer)
    fullerton = db.Column(db.Integer)
    buena_park = db.Column(db.Integer)
    irvine = db.Column(db.Integer)
    costa_mesa = db.Column(db.Integer)
    westminster = db.Column(db.Integer)
    newport_beach = db.Column(db.Integer)
    la_habra = db.Column(db.Integer)
    tustin = db.Column(db.Integer)
    placentia = db.Column(db.Integer)
    stanton = db.Column(db.Integer)
    mission_viejo = db.Column(db.Integer)
    yorba_linda = db.Column(db.Integer)
    lake_forest = db.Column(db.Integer)
    cypress = db.Column(db.Integer)
    fountain_valley = db.Column(db.Integer)
    seal_beach = db.Column(db.Integer)
    san_clemente = db.Column(db.Integer)
    los_alamitos = db.Column(db.Integer)
    brea = db.Column(db.Integer)
    san_juan_capistrano = db.Column(db.Integer)
    laguna_niguel = db.Column(db.Integer)
    aliso_viejo = db.Column(db.Integer)
    laguna_hills = db.Column(db.Integer)
    laguna_beach = db.Column(db.Integer)
    rancho_santa_margarita = db.Column(db.Integer)
    dana_point = db.Column(db.Integer)
    la_palma = db.Column(db.Integer)
    midway_city = db.Column(db.Integer)
    ladera_ranch = db.Column(db.Integer)
    trabuco_canyon = db.Column(db.Integer)
    villa_park = db.Column(db.Integer)
    laguna_woods = db.Column(db.Integer)
    rossmoor = db.Column(db.Integer)
    rancho_mission_viejo = db.Column(db.Integer)
    coto_de_caza = db.Column(db.Integer)
    silverado = db.Column(db.Integer)
