"""
A module designed to hold the logic related to the contribution page.
"""

import bisect
import csv
from datetime import datetime
from typing import Dict, List

from coa_flask_app.db_accessor import Accessor


def get_tls() -> List[str]:
    """
    Get all the team leads for the drop downs.

    Returns:
        The list of all the team leads.
    """
    query = """
            SELECT
                DISTINCT team_captain
            FROM coa.team_info
            ORDER BY team_captain
            """
    with Accessor() as db_handle:
        db_handle.execute(query)
        return [tl[0] for tl in db_handle.fetchall()]


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
            # This handles inserting in sorted order
            bisect.insort(trash_items[material], item)
        else:
            trash_items[material] = [item]

    return trash_items


def insert_contribution(post_str: str) -> None:
    """
    Inserts into the database that a contribution was made.
    """
    # TODO: This should be changed as this is all tied to how the
    # data was passed in the older version.
    team_query = """
                INSERT INTO coa.team_info
                    (site_id,
                     volunteer_date,
                     team_captain,
                     num_of_people,
                     num_of_trashbags,
                     trash_weight,
                     walking_distance,
                     updated_by)
                VALUES
                """

    volunteer_query = """
                      INSERT INTO coa.volunteer_info
                        (team_id,
                         item_id,
                         quantity,
                         brand,
                         updated_by,
                         event_code)
                    VALUES
                    """

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

    query = f"""BEGIN;
                {team_query}';
                {volunteer_query[:-1]};
                COMMIT;
             """
    with Accessor() as db_handle:
        db_handle.execute(query)
