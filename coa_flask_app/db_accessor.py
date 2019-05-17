"""
The module designed to contain all the database access logic.
"""

import os
from typing import List, Tuple

import pymysql


class Accessor:
    """
    This class is designed to contain all the database access logic.
    """

    def __init__(self) -> None:
        """
        The constructor of the Accessor class.

        We create a database connection to be used.
        """
        self.connection = pymysql.connect(host=os.environ['DB_SERVER'],
                                          user=os.environ['DB_USERNAME'],
                                          password=os.environ['DB_PASSWORD'],
                                          database=os.environ['DB_DATABASE'],
                                          port=int(os.environ['DB_PORT']))

    def show_tables(self) -> List[str]:
        """
        Returns all the tables in the database.

        Returns:
            The name of all the tables.
        """
        query = 'SHOW TABLES'
        with self.connection as cursor:
            cursor.execute(query)
            return [table_tuple[0] for table_tuple in cursor.fetchall()]

    def all_locations(self) -> List[Tuple[str, str, str]]:
        """
        Returns a list of tuples comprising of the distinct sites,
        towns and counties.

        For example:
        [
            ("Atlantic City", "Atlantic City", "Atlantic"),
            ("New Jersey Ave", "Atlantic City", "Atlantic"),
            ...
        ]

        Returns:
            A list of tuples.
        """
        query = """
                SELECT
                    DISTINCT coa_summary_view.site_name,
                    coa_summary_view.town,
                    coa_summary_view.county
                FROM coa.coa_summary_view
                """
        with self.connection as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def item_breakdown(self,
                       location_category: str,
                       location_name: str,
                       start_date: str,
                       end_date: str) -> List[Tuple[int, str, str, str, int]]:
        """
        Returns a list of tuples comprising of the item id, item name, category,
        material, and quantity.

        For example:
        [
            ...
        ]

        Args:
            location_category: The type of location.
            location_name: The name of the location.
            start_date: The start date.
            end_date: The end date.

        Returns:
            A list of item id, item name, category, material, quantity.
        """
        if location_category not in {'site_name', 'town', 'county'}:
            return []

        query = """
                 SELECT
                     item_id,
                     item_name,
                     category,
                     material,
                     SUM(quantity) AS quantity_sum
                 FROM coa_summary_view
                 WHERE %s <= volunteer_date
                     AND volunteer_date <= %s
                     AND """ + location_category + """ = %s
                 GROUP BY item_name
                 """
        with self.connection as cursor:
            cursor.execute(query, (start_date,
                                   end_date,
                                   location_name))
            return cursor.fetchall()
