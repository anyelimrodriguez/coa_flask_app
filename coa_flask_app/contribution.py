"""
A module designed to hold the logic related to the contribution page.
"""

import bisect
import csv
from datetime import datetime
from typing import Dict, List, Tuple

from coa_flask_app.db_accessor import Accessor


def get_sites() -> List[Tuple[str, str]]:
    """
    Get all the sites for the drop downs.

    Returns:
        The list of site id and a comma seperated list of features
        about a site.
    """
    # TODO: This can't look pretty in the end, or be needed, will probably tweak.
    query = """
            SELECT
                site_id,
                site_name,
                street,
                town,
                county,
                state,
                zipcode
            FROM coa.site
            ORDER BY county, town, street
            """
    with Accessor() as db_handle:
        db_handle.execute(query)
        return [(row[0], ', '.join(row[1:]))
                for row in db_handle.fetchall()]


def get_tls() -> List[str]:
    """
    Get all the TLs for the drop downs.

    Returns:
        The list of all the TLs.
    """
    query = """
            SELECT
                DISTINCT team_captain
            FROM coa.team_info
            ORDER BY team_captain
            """
    with Accessor() as db_handle:
        db_handle.execute(query)
        return [tl[0] for tl in db_handle.fetchall(query)]


def get_trash_items() -> Dict[str, List[str]]:
    """
    Get all the trash items for the drop downs.

    Returns:
        The mapping of material to trash items.
    """
    query = """
            SELECT
                DISTINCT item_id,
                material,
                category,
                item_name
            FROM coa.item
            """
    with Accessor() as db_handle:
        db_handle.execute(query)
        items = [(row[1],
                  f'{row[2]}, {row[3]}[{row[0]}]')
                 for row in db_handle.fetchall()]

    trash_items: Dict[str, List[str]] = {}
    for material, item in items:
        if material in trash_items:
            bisect.insort(trash_items[material], item)
        else:
            trash_items[material] = [item]

    return trash_items


def insert_contribution(imd):
    # TODO
    team_query = """
    INSERT INTO coa.team_info
    (site_id,volunteer_date,team_captain,num_of_people,num_of_trashbags
    ,trash_weight,walking_distance,updated_by)
    VALUES
    """

    volunteer_query = """
    INSERT INTO coa.volunteer_info (team_id,item_id,quantity,brand,updated_by,event_code)
    VALUES
    """

    post_str = imd.items()[0][0]
    team_info, volunteer_info = post_str.split('----')

    row = team_info.split('#')
    team_query += "(%s,'%s','%s',%s,%s,%s,%s,'%s')" % (
        row[0],
        datetime.strptime(row[1], '%m/%d/%Y').strftime("%Y-%m-%d"),
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7]
    )

    volunteer_reader = csv.reader(volunteer_info.split('||'), delimiter='#')
    for row in volunteer_reader:
        if row:
            volunteer_query += "(%s,%s,%s,'%s','%s','%s')," % (
                'LAST_INSERT_ID()',
                row[0].split('[')[1].split(']')[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )

    query = "BEGIN; " + team_query + "; " + volunteer_query[:-1] + "; COMMIT;"
    return query
