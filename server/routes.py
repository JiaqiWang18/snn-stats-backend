from flask import jsonify, render_template, request
from server import app
from sqlalchemy import and_
from server import db, models, schema
import pytz
from datetime import datetime, timedelta, date


def get_current_date():
    pacific_time = pytz.timezone('US/Pacific')
    return datetime.now(pacific_time).date()


def get_by_date(current_date):
    data = lambda model, sch: sch.dump(db.session.query(model).get(current_date))
    return {
        "United States": data(models.UnitedStates, schema.UnitedStatesSchema()),
        "California": data(models.California, schema.CaliforniaSchema()),
        "LA County": data(models.LACounty, schema.LACountySchema()),
        "Orange County": data(models.OrangeCounty, schema.OrangeCountySchema()),
        "Orange County Cities": data(models.OCCities, schema.OCCitiesSchema())
    }


@app.route("/")
def index():
    return "Hello"


@app.route('/get')
def get_display_data():
    # 2020-12-31
    user_date = request.args.get('date')
    if user_date:
        user_date = [int(sub) for sub in user_date.split("-")]
        current_date = date(user_date[0], user_date[1], user_date[2])
    else:
        current_date = get_current_date()
    yesterday_date = current_date - timedelta(1)

    current_stats = get_by_date(current_date)
    yesterday_stats = get_by_date(yesterday_date)

    output = {}
    for key in current_stats:
        output[key] = {}
        for inner_key in current_stats[key]:
            if inner_key != 'date':
                try:
                    output[key][inner_key] = [
                        current_stats[key][inner_key],
                        current_stats[key][inner_key] - yesterday_stats[key][inner_key]
                    ]
                except KeyError:
                    pass

    return {current_date.strftime("%m/%d/%Y"): output}

@app.route("/graph-data")
def get_graph_data():
    model_name = request.args.get('model')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not model_name or not start_date:
        return "Please provide a model and start"
    if not end_date:
        end_date = get_current_date()
    mapper = {'us': [models.UnitedStates, schema.UnitedStatesSchema()],
              'oc': [models.OrangeCounty, schema.OrangeCountySchema()],
              'la': [models.LACounty, schema.LACountySchema()],
              'ca': [models.California, schema.CaliforniaSchema()]}
    model = mapper[model_name][0]
    qry = db.session.query(model).filter(
        and_(model.date >= start_date, model.date <= end_date)).all()

    return jsonify([mapper[model_name][1].dump(data) for data in qry])
