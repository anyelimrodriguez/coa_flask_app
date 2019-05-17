"""
The module designed to contain all the database access logic.
"""

import os
from typing import List

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

    def all_locations(category: str) -> List[str]:
        with self.connection as cursor:
            query = """
                    SELECT DISTINCT %s
                    """
            cursor.execute(query, category)
            return [i[0] for i in cursor.fetchall()]

