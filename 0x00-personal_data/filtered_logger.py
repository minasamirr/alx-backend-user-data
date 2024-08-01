#!/usr/bin/env python3
"""
Module for filtering log data.
"""

import re
from typing import List, Tuple
import logging
import os
import mysql.connector
from mysql.connector import connection


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message obfuscated.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all
        fields in the log line (message).

    Returns:
        The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with a list of fields to redact.

        Args:
            fields: A list of strings representing the fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redact specified fields.

        Args:
            record: The log record to format.

        Returns:
            The formatted and redacted log record.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger named "user_data".

    Returns:
        A logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connect to a secure database and return the connection object.

    Returns:
        A mysql.connector.connection.MySQLConnection object.
    """
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )


def main():
    """
    Retrieves and prints all rows in the users table with fields filtered.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    logger = get_logger()
    for row in rows:
        message = "name={}; email={}; phone={}; ssn={}; password={}; ip={}; last_login={}; user_agent={};".format(*row)
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
