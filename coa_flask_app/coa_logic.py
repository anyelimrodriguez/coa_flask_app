"""
A module designed to hold the buisness logic of the routes the Flask app serves.
"""

import heapq
from typing import Any, Dict, List

from coa_flask_app import db_accessor


def all_locations_list() -> List[Dict[str, Any]]:
    """
    Returns all the locations by category.

    NOTICE: To be deprecated by the locations_hierarchy function.

    For example:
    [{
      "locationCategory": "site",
      "locationLabel": "Site",
      "locationNames": [
        "14 Ave ",
        "14th & 15th Ave",
        ...
      ]},
      ...
    ]

    Returns:
        A json list of the locations by category.
    """
    locations_tuples = db_accessor.Accessor().all_locations()
    names = 'locationNames'
    site_data = {
        'locationCategory': 'site',
        'locationLabel': 'Site',
        names: sorted({i[0] for i in locations_tuples})
    }
    town_data = {
        'locationCategory': 'town',
        'locationLabel': 'Town',
        names: sorted({i[1] for i in locations_tuples})
    }
    county_data = {
        'locationCategory': 'county',
        'locationLabel': 'County',
        names: sorted({i[2] for i in locations_tuples})
    }
    return [site_data, town_data, county_data]


def dirty_dozen(location_category: str,
                location_name: str,
                start_date: str,
                end_date: str) -> List[Dict[str, Any]]:
    """
    Returns the top 12 items with the most debris along with its
    associated meta data.

    Args:
        location_category: The category of location, site, town, or county.
        location_name: The name of the location.
        start_date: The start date for our query.
        end_date: The end date for our query.

    Returns:
        A list of the dirty dozen.
    """
    result = db_accessor.Accessor().item_breakdown(location_category,
                                                   location_name,
                                                   start_date,
                                                   end_date)
    dozen = heapq.nlargest(12, result, key=lambda x: x[-1])
    total = sum(count for *_, count in result)
    wrap_for_response = lambda item_id, name, category, material, count, total: {
        'itemName': name,
        'itemId': item_id,
        'categoryName': category,
        'materialName': material,
        'count': count,
        'percentage': count / total * 100
    }

    return [wrap_for_response(item_id, name, category, material, count, total)
            for item_id, name, category, material, count in dozen]


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
        if child['name'] == name:
            return index

    return -1


def breakdown(location_category: str,
              location_name: str,
              start_date: str,
              end_date: str) -> Dict[str, Any]:
    """
    Returns the breakdown of the all the different types of debris.

    Args:
        location_category: The category of location, site, town, or county.
        location_name: The name of the location.
        start_date: The start date for our query.
        end_date: The end date for our query.

    Returns:
        A json breakdown of the debris.
    """
    result = db_accessor.Accessor().item_breakdown(location_category,
                                                   location_name,
                                                   start_date,
                                                   end_date)
    # Aggregate items into material and category hierarchy for sunburst chart
    sunburst_data: Dict[str, Any] = {'name': 'Debris', 'children': []}
    for _, item_name, category_name, material_name, count in result:
        # Check if this material has already been added
        material_idx = get_child(material_name, sunburst_data['children'])
        if material_idx < 0:
            sunburst_data['children'].append(
                {'name': material_name, 'children': []})
            material_idx = len(sunburst_data['children']) - 1

        # Check if this category has already been added
        material = sunburst_data['children'][material_idx]
        category_idx = get_child(category_name, material['children'])
        if category_idx < 0:
            sunburst_data['children'][material_idx]['children'].append(
                {'name': category_name, 'children': []})
            category_idx = len(material['children']) - 1

        material['children'][category_idx]['children'].append(
            {'name': item_name, 'count': count})

    return sunburst_data


def valid_date_range(location_category: str,
                     location_name: str) -> Dict[str, str]:
    """
    Returns the date range for a location.

    Args:
        location_category: The category of location, site, town, or county.
        location_name: The name of the location.

     Returns:
        The date range.
     """
    result = db_accessor.Accessor().date_range(location_category,
                                               location_name)
    if result is None:
        return {}

    first, last = result
    return {
        'firstDate': first.strftime('%Y-%m-%d'),
        'lastDate': last.strftime('%Y-%m-%d')
    }


def locations_hierarchy() -> Dict[str, Dict[str, List[str]]]:
    """
    Returns all the locations in a hierarchy.

    For example:
    {
        "Atlantic": {
          "Atlantic City": [
            "Atlantic City",
            "New Jersey Ave",
            "Missouri Ave",
            "Atlantic Highlands Harbor"
          ],
          ...
        }
    }

    Returns:
        A json list of the locations hierarchy.
    """
    locations_tuples = db_accessor.Accessor().all_locations()
    hierarchy: Dict[str, Dict[str, List[str]]] = {}
    for site, town, county in locations_tuples:
        if county not in hierarchy:
            hierarchy[county] = {town: [site]}
            continue

        h_county = hierarchy[county]
        if town not in h_county:
            h_county[town] = [site]
            continue

        h_county[town].append(site)

    return hierarchy
