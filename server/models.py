from server import db


class OrangeCounty(db.Model):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    total_tested = db.Column(db.Integer)


class LACounty(db.Model):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)


class California(db.Model):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)


class UnitedStates(db.Model):
    date = db.Column(db.Date, primary_key=True)
    total_cases = db.Column(db.Integer)
    death = db.Column(db.Integer)
    recovered = db.Column(db.Integer)

