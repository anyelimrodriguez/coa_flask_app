"""
The module designed to contain all the database access logic.
"""

import os
from typing import  Dict, List

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

    def all_locations() -> List[Tuple[str, str, str]]:
        """
        Returns a list of tuples comprising of the distinct sites,
        towns and counties.

        For example: 
            [[<site1>,<town1><count1>],...]

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

            