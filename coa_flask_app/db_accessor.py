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
        self.cursor = None

    def __enter__(self):
        """
        The enter of the Accessor class.

        Returns:
            A cursor to execute queries on.
        """
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self,
                 ex_type,
                 ex_value,
                 traceback) -> None:
        """
        The exit of the Accessor class.

        This cleans up the cursor and database connection.

        Args:
            ex_type: The exception type.
            ex_value: The exception value.
            traceback: The traceback for the exception.
        """
        _, _, _ = ex_type, ex_value, traceback
        self.connection.commit()
        if self.cursor is not None:
            self.cursor.close()

        self.connection.close()

    def show_tables(self) -> List[str]:
        """
        Returns all the tables in the database.

        Returns:
            The name of all the tables.
        """
        query = 'SHOW TABLES'
        with self.connection as cursor:
            cursor.execute(query)
            return [columns[0] for columns in cursor.fetchall()]
