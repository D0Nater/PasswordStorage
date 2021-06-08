# -*- coding: utf-8 -*-

import sqlite3


class DatabaseControl:
    """ DatabaseControl

    Methods
    -------
    open_db : `instancemethod`
    close_db : `instancemethod`
    commit_db : `instancemethod`
    execute_query : `instancemethod`

    Examples
    --------
    >>> db_control = DatabaseControl(file="database.sqlite")
    >>> db_control.open_db()
    >>> db_control.execute_query("CREATE TABLE IF NOT EXISTS TEST_TABLE (COLUMN1, COLUMN2)")
    >>> db_control.execute_query("INSERT INTO TEST_TABLE VALUES (?, ?)", ("data1", "data2"))
    >>> db_control.close_db()

    >>> db_control = DatabaseControl()
    >>> db_control.open_db(file="database.sqlite")
    >>> db_control.execute_query("SELECT * FROM TEST_TABLE")
    >>> db_control.close_db()
    """

    def __init__(self, file):
        """
        Parameters
        ----------
        file : |str|, required
            Name of database file to use
        """

        self._DATABASE_FILE = file

    def open_db(self, file=None):
        """
        Parameters
        ----------
        file : |str| or ``None``, required / (optional if you want open file from method `__init__`)
            Name of database file to open
        """

        self._DATABASE_FILE = file if file is not None else self._DATABASE_FILE
        self._conn = sqlite3.connect(self._DATABASE_FILE)
        self._cursor = self._conn.cursor()

    def close_db(self):
        """ Function for closing database connection """

        self._conn.close()

    def commit_db(self):
        """ Function for saving changes to database """

        self._conn.commit()

    def execute_query(self, query, args=()):
        """ Function for making a request to database and getting a response

        Parameters
        ----------
        query : |str|, required
            Request to execute to database
        args : |tuple|, optional
            Arguments for request

        Returns
        -------
        :class:`str` or ``None``
            Database response
        """

        self._cursor.execute(query, (*args, ))
        self.commit_db()

        return self._cursor.fetchall()
