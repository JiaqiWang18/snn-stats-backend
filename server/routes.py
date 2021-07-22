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
    return "SNN COVID-19 Data API"


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
    #print(current_stats)
    yesterday_stats = get_by_date(yesterday_date)
    #print(yesterday_stats)

    output = {}
    for key in current_stats:
        output[key] = {}
        for inner_key in current_stats[key]:
            #print(inner_key)
            if inner_key != 'date' and current_stats[key][inner_key] is not None and inner_key in yesterday_stats[
                key] and yesterday_stats[key][inner_key] is not None:
                try:
                    output[key][inner_key] = [
                        current_stats[key][inner_key],
                        current_stats[key][inner_key] - yesterday_stats[key][inner_key]
                    ]
                except KeyError:
                    pass

    return {current_date.strftime("%Y-%m-%d"): output}


@app.route("/graph-data")
def get_graph_data():
    mapStrToModelCol = lambda model: {
        "total_cases": model.total_cases,
        "death": model.death,
        "recovered": model.recovered,
        "total_tested": model.total_tested
    }
    data_type = request.args.get('type')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not end_date:
        end_date = get_current_date()
    mapper = {'us': [models.UnitedStates, schema.UnitedStatesSchema(many=True)],
              'oc': [models.OrangeCounty, schema.OrangeCountySchema(many=True)],
              'la': [models.LACounty, schema.LACountySchema(many=True)],
              'ca': [models.California, schema.CaliforniaSchema(many=True)]}
    output = {}
    for location in mapper:
        model = mapper[location][0]
        current_schema = mapper[location][1]
        output[location] = current_schema.dump(db.session.query(model.date, mapStrToModelCol(model)[data_type]).filter(
            and_(model.date >= start_date, model.date <= end_date, )).all())

    return jsonify(output)


if __name__ == '__main__':
    print(get_by_date())
