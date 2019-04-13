"""
The main entrance to the flask app.

This includes the setting up of flask as well as all of the routes for
the application.
"""


from typing import List, Tuple

from flask import jsonify, request, url_for
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from coa_flask_app import coa_logic


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

app.config.from_pyfile('config.py')

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()


def routes():
    """
    A function to retrieve all routes installed in the app.

    Returns:
        A list of all the routes installed in the app.
    """
    return [str(rule) for rule in app.url_map.iter_rules()]


@app.route('/')
def index():
    return jsonify(routes())


@app.route('/sitecategoriesbreakdown')
def site_details():
    location_category = request.args.get('locationCategory',
                                         default='site', type=str)
    site_id = request.args.get('siteId', default=0, type=int)
    location_name = request.args.get('locationName',
                                     default='Union Beach', type=str)

    return jsonify(coa_logic.site_details(location_category,
                                          site_id,
                                          location_name))

@app.route('/getsitesdropdownlist')
def site_list():
    return jsonify(site_names=coa_logic.site_list())


@app.route('/locations')
def all_locations_list():
    return jsonify(locations=coa_logic.all_locations_list())


@app.route('/dirtydozen')
def dirty_dozens():
    location_category = request.args.get(
        'locationCategory', default='site', type=str)
    location_name = request.args.get(
        'locationName', default='Union Beach', type=str)
    start_date_str = request.args.get(
        'startDate', default='2016-1-1', type=str)
    end_date_str = request.args.get('endDate', default='2018-12-31', type=str)

    return jsonify(dirtydozen=coa_logic.dirty_dozen(location_category,
                                                    location_name,
                                                    start_date_str,
                                                    end_date_str))


@app.route('/breakdown')
def breakdown():
    location_category = request.args.get(
        'locationCategory', default='site', type=str)
    location_name = request.args.get(
        'locationName', default='Union Beach', type=str)
    start_date_str = request.args.get(
        'startDate', default='2016-1-1', type=str)
    end_date_str = request.args.get('endDate', default='2018-12-31', type=str)

    return jsonify(data=coa_logic.breakdown(location_category,
                                            location_name,
                                            start_date_str,
                                            end_date_str))


@app.route('/validdaterange')
def valid_date_range():
    location_category = request.args.get(
        'locationCategory', default='site', type=str)
    location_name = request.args.get(
        'locationName', default='Union Beach', type=str)

    return jsonify(validDateRange=coa_logic.valid_date_range(location_category,
                                                             location_name))


@app.route('/validmaterials')
def valid_materials():
    location_category = request.args.get(
        'locationCategory', default=None, type=str)
    locations = request.args.getlist('locations[]', type=str)

    return jsonify(materials=coa_logic.valid_materials(location_category,
                                                       locations))


@app.route('/itemslist')
def items_list():
    item_type = request.args.get('itemType', default='category', type=str)

    return jsonify(items_list=coa_logic.items_list(item_type))


@app.route('/trends')
def trends():
    location_category = request.args.get(
        'locationCategory', default=None, type=str)
    locations = request.args.getlist('locations[]', type=str)

    return jsonify(data=coa_logic.trends(location_category, locations))
