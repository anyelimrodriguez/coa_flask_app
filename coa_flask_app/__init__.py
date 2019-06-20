"""
The main entrance to the flask app.

This includes the setting up of flask as well as all of the routes for
the application.
"""


from datetime import datetime
from typing import Any, Dict, List, Tuple, Union

from flask import jsonify, request, url_for
from flask import Flask
from flask_cors import CORS

from coa_flask_app import site


# Recursive types not yet fully supported.
#
# JSONInnerType = Union[int, bool, str, JSON]
# JSON = Union[Dict[str, JSONInnerType], List[JSONInnerType]]
#
JSON = Union[Dict[str, Any], List[Any]]

APP = Flask(__name__)
CORS(APP)


@APP.route('/')
def index() -> JSON:
    """
    Index holds the main page for the REST API.

    This is mainly designed to send over a list of valid routes.

    Returns:
        The json list of valid routes.
    """
    return jsonify([str(rule) for rule in APP.url_map.iter_rules()])


@APP.route('/locations')
def all_locations_list() -> JSON:
    """
    The locations route returns all the locations.

    Returns:
        A json list of all the locations.
    """
    return jsonify(locations=site.all_locations_list())


@APP.route('/dirtydozen')
def dirty_dozen() -> JSON:
    """
    The dirty dozen route is designed to give the UI the data
    for a dirty dozen.

    The app route itself contains:
        locationCategory - Default of site.
        locationName     - Default of the common location.
        startDate        - The old start date for historical reasons.
        endDate          - Now.

    Returns:
        The dirty dozen for the requested category, name, and date range.
    """
    location_category = request.args.get('locationCategory',
                                         default='site',
                                         type=str)
    location_category = 'site_name' if location_category == 'site' else location_category

    location_name = request.args.get('locationName',
                                     default='Union Beach',
                                     type=str)
    start_date = request.args.get('startDate',
                                  default='2016-1-1',
                                  type=str)
    end_date = request.args.get('endDate',
                                default=datetime.now().strftime('%Y-%m-%d'),
                                type=str)

    return jsonify(dirtydozen=site.dirty_dozen(location_category,
                                               location_name,
                                               start_date,
                                               end_date))


@APP.route('/breakdown')
def breakdown() -> JSON:
    """
    The breakdown route is designed to give the UI the data
    for a breakdown.

    The app route itself contains:
        locationCategory - Default of site.
        locationName     - Default of the common location.
        startDate        - The old start date for historical reasons.
        endDate          - Now.

    Returns:
        The breakdown for the requested category, name, and date range.
    """
    location_category = request.args.get('locationCategory',
                                         default='site',
                                         type=str)
    location_category = 'site_name' if location_category == 'site' else location_category

    location_name = request.args.get('locationName',
                                     default='Union Beach',
                                     type=str)
    start_date = request.args.get('startDate',
                                  default='2016-1-1',
                                  type=str)
    end_date = request.args.get('endDate',
                                default=datetime.now().strftime('%Y-%m-%d'),
                                type=str)

    return jsonify(data=site.breakdown(location_category,
                                       location_name,
                                       start_date,
                                       end_date))


@APP.route('/validdaterange')
def valid_date_range() -> JSON:
    """
    The valid date range route is designed to give the UI a valid date
    range.

    The app route itself contains:
        locationCategory - Default of site.
        locationName     - Default of the common location.

    Returns:
        The valid date range for the requested category and name.
    """
    location_category = request.args.get('locationCategory',
                                         default='site',
                                         type=str)
    location_category = 'site_name' if location_category == 'site' else location_category

    location_name = request.args.get('locationName',
                                     default='Union Beach',
                                     type=str)

    return jsonify(validDateRange=site.valid_date_range(location_category,
                                                        location_name))


@APP.route('/locationsHierarchy')
def locations_hierarchy() -> JSON:
    """
    The locations hierarchy route returns the all the locations in a hierarchy.

    Returns:
        A json list of the locations hierarchy.
    """
    return jsonify(locationsHierarchy=site.locations_hierarchy())


@APP.route('/contribution')
def contribution() -> JSON:
    pass


@APP.route('/updatedb', methods=['POST'])
def updatedb():
    try:
        query = contribution.create_query(request.form)
        db.insert(query)
        return 'Your records have been successfully saved!'
    except:
        return """Your records failed in saving to db.
Please make sure you have all fields filled properly!"""
