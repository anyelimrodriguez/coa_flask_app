"""
A module designed to hold the buisness logic of the routes the Flask app serves.
"""

import datetime
from typing import Any, Dict, List

from coa_flask_app import db_accessor
from coa_flask_app.models import CoaSummaryView


LOCATION_CATEGORIES = {
    "site": {
        "label": "Site",
        "column": CoaSummaryView.site_name
    },
    "town": {
        "label": "Town",
        "column": CoaSummaryView.town
    },
    "county": {
        "label": "County",
        "column": CoaSummaryView.county
    }
}

ITEM_TYPES = {
    "material": CoaSummaryView.material,
    "category": CoaSummaryView.category,
    "item_name": CoaSummaryView.item_name
}


def get_location_category_column(location_category):
    location_category = location_category if location_category in LOCATION_CATEGORIES else "site"
    return LOCATION_CATEGORIES[location_category]["column"]


def site_list():
    sql_result = CoaSummaryView.query.filter().\
        with_entities(CoaSummaryView.site_name).\
        group_by(CoaSummaryView.site_name).\
        order_by(CoaSummaryView.site_name).\
        all()
    json_list = list()
    for row in sql_result:
        if len(row) == 1:
            print(row)
            json_list.append(row[0])

    return json_list


def create_location_dict(category, label, location_sql_result):
    location_list = list(filter(lambda item: item[0], location_sql_result))
    location_list = [x[0] for x in location_list]
    location_dict = {}
    location_dict['locationCategory'] = category
    location_dict['locationLabel'] = label
    location_dict['locationNames'] = location_list
    return location_dict


def all_locations_list():
    result_list = list()

    for category, category_info in LOCATION_CATEGORIES.items():
        sql_result = CoaSummaryView.query.filter().\
            with_entities(category_info["column"]).\
            group_by(category_info["column"]).\
            order_by(category_info["column"]).\
            all()
        result_list.append(create_location_dict(
            category, category_info["label"], sql_result))

    return result_list


def parse_date_string(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def dirty_dozen(location_category, location_name, start_date_str, end_date_str):
    location_category_column = get_location_category_column(location_category)

    # convert date strings to dates
    start_date = parse_date_string(start_date_str)
    end_date = parse_date_string(end_date_str)

    result = CoaSummaryView.query \
        .filter(
            location_category_column == location_name,
            CoaSummaryView.volunteer_date >= start_date,
            CoaSummaryView.volunteer_date <= end_date) \
        .with_entities(
            CoaSummaryView.item_name,
            CoaSummaryView.item_id,
            CoaSummaryView.category,
            CoaSummaryView.material,
            db.func.sum(CoaSummaryView.quantity).label("quantity_sum")) \
        .group_by(CoaSummaryView.item_name) \
        .order_by("quantity_sum desc") \
        .limit(12)

    total_items = CoaSummaryView.query \
        .filter(
            location_category_column == location_name,
            CoaSummaryView.volunteer_date >= start_date,
            CoaSummaryView.volunteer_date <= end_date) \
        .with_entities(db.func.sum(CoaSummaryView.quantity)) \
        .scalar()

    return [{
        'itemName': row[0],
        'itemId': row[1],
        'categoryName': row[2],
        'materialName': row[3],
        'count': row[4],
        'percentage': 0 if total_items is None else row[4] / total_items * 100
    }
            for row in result]


def breakdown(location_category, location_name, start_date_str, end_date_str):
    location_category_column = get_location_category_column(location_category)

    # convert date strings to dates
    start_date = parse_date_string(start_date_str)
    end_date = parse_date_string(end_date_str)

    result = CoaSummaryView.query \
        .filter(
            location_category_column == location_name,
            CoaSummaryView.volunteer_date >= start_date,
            CoaSummaryView.volunteer_date <= end_date) \
        .with_entities(
            CoaSummaryView.item_name,
            CoaSummaryView.item_id,
            CoaSummaryView.category,
            CoaSummaryView.material,
            db.func.sum(CoaSummaryView.quantity).label("quantity_sum")) \
        .group_by(CoaSummaryView.item_name)

    # Aggregate items into material and category hierarchy for sunburst chart
    sunburst_data = {"name": "Debris", "children": []}
    for item in result:
        itemName = item[0]
        itemId = item[1]
        categoryName = item[2]
        materialName = item[3]
        count = item[4]

        # Check if this material has already been added
        materialIdx = get_child(materialName, sunburst_data["children"])
        if materialIdx < 0:
            sunburst_data["children"].append(
                {"name": materialName, "children": []})
            materialIdx = len(sunburst_data["children"]) - 1

        # Check if this category has already been added
        material = sunburst_data["children"][materialIdx]
        categoryIdx = get_child(categoryName, material["children"])
        if categoryIdx < 0:
            sunburst_data["children"][materialIdx]["children"].append(
                {"name": categoryName, "children": []})
            categoryIdx = len(material["children"]) - 1

        material["children"][categoryIdx]["children"].append(
            {"name": itemName, "count": count})

    return sunburst_data


def get_child(name: str, children: List[Dict[str, Any]]) -> int:
    """
    Returns the index of the first name of the child that matches the
    name provided.

    Args:
        name: The name of the child.
        children: The list of children.

    Returns:
        The index of the first child matching that name.
        If none exist, return -1.
    """
    for index, child in enumerate(children):
        if child["name"] == name:
            return index

    return -1


def valid_date_range(location_category, location_name):
    location_category_column = get_location_category_column(location_category)

    db_result = CoaSummaryView.query \
        .filter(location_category_column == location_name) \
        .with_entities(
            db.func.min(CoaSummaryView.volunteer_date),
            db.func.max(CoaSummaryView.volunteer_date)) \
        .all()

    # db_result should have only one value
    result_dict = dict()
    for first_date, last_date in db_result:
        result_dict["firstDate"] = first_date.strftime('%Y-%m-%d')
        result_dict["lastDate"] = last_date.strftime('%Y-%m-%d')

    return result_dict
