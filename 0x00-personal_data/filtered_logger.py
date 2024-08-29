#!/usr/bin/env python3
"""
This module:
- contains a function to obfuscate
specific fields in a log message.
- defines a RedactingFormatter class to filter
sensitive information from log messages.
- provides a logger that obfuscates
sensitive information in logs.
- provides a function to securely connect to a
MySQL database using environment variables.
- connects to a database, retrieves user data,
and logs it with sensitive fields obfuscated.
"""

import logging
import mysql.connector
from mysql.connector import connection
from mysql.connector.connection import MySQLConnection
# from mysql.connector.abstracts import MySQLConnectionAbstract
# from mysql.connector import MySQLConnection
# from mysql.connector.pooling import PooledMySQLConnection
import os
import re
from typing import cast, List, Tuple
# from typing import Union


# Define a constant tuple for PII fields that should be redacted in logs.
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscate the specified fields in the log message.

    Args:
        fields (List[str]): The list of fields to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The log message containing the fields.
        separator (str): The character separating
        the fields in the log message.

    Returns:
        str: The log message with obfuscated fields.
    """
    # Create a regex pattern that matches
    # any of the fields to be obfuscated.
    # The pattern looks for 'field_name=' followed by
    # any character until it reaches the separator.
    # Join all field names with '|' to create alternatives in regex.
    fields_pattern = '|'.join(fields)
    # Create the full regex pattern.
    regex_pattern = r'({})=.+?{}'.format(fields_pattern, separator)

    # Create the replacement pattern, which keeps the field name
    # but replaces its value with the redaction string.
    replacement_pattern = r'\1={}{}'.format(redaction, separator)

    # Use re.sub to replace the matched fields
    # with their redacted versions in the message.
    obfuscated_message = re.sub(regex_pattern, replacement_pattern, message)

    # Return the obfuscated message.
    # return obfuscated_message
    return re.sub(r'({})=.+?{}'.format('|'.join(fields),
                  separator), r'\1={}{}'.format(redaction,
                                                separator), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for
    filtering PII data in log messages. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with a list of fields to redact.

        Args:
            fields (List[str]): The list of fields
            to obfuscate in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        # Store the fields to be redacted.
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, filtering out sensitive information.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with
            redacted sensitive information.
        """
        # Obfuscate the sensitive fields in the log message.
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        # Format the log record using the parent class's format method.
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named 'user_data'
    with a StreamHandler and a RedactingFormatter
    that obfuscates sensitive information.

    Returns:
        logging.Logger: Configured logger object instance.
    """
    # Create a logger named 'user_data'.
    logger = logging.getLogger("user_data")

    # Set the logging level to INFO, so it logs messages up to INFO level.
    logger.setLevel(logging.INFO)

    # Prevent the logger from propagating messages to other loggers.
    logger.propagate = False

    # Create a StreamHandler to output logs to the console (stdout).
    stream_handler = logging.StreamHandler()

    # Set the formatter for the handler using
    # RedactingFormatter, passing in the PII_FIELDS.
    stream_handler.setFormatter(RedactingFormatter(fields=list(PII_FIELDS)))

    # Add the handler to the logger.
    logger.addHandler(stream_handler)

    # Return the configured logger.
    return logger


# def get_db() -> Union[MySQLConnectionAbstract, PooledMySQLConnection]:
def get_db() -> connection.MySQLConnection:
    """
    Connect to the MySQL database using credentials from environment variables.

    The function retrieves the database connection
    parameters from environment variables:
    - PERSONAL_DATA_DB_USERNAME: The database username (default: "root").
    - PERSONAL_DATA_DB_PASSWORD: The database password
    (default: an empty string).
    - PERSONAL_DATA_DB_HOST: The database host (default: "localhost").
    - PERSONAL_DATA_DB_NAME: The name of the database.

    Returns:
        mysql.connector.connection.MySQLConnection:
        A MySQL database connection object.
    """
    # Fetch environment variables for database connection details.
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish and return the database
    # connection using the provided credentials.
    return cast(MySQLConnection, mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    ))


def main():
    """
    Main function that fetches user data from the database
    and logs it with sensitive fields obfuscated.
    """
    # Get the database connection and logger.
    db = get_db()
    logger = get_logger()

    # Execute the SQL query to fetch all user data.
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    # Get column names to format the log message.
    # columns = [desc[0] for desc in cursor.description]
    # if cursor.description is not None else []
    if cursor.description is not None:
        columns = []
        for desc in cursor.description:
            columns.append(desc[0])
        else:
            columns = []

    # Log each row with sensitive data obfuscated.
    for row in cursor.fetchall():
        message = "; ".join(f"{col}={val}" for col,
                            val in zip(columns, row))
        logger.info(message)

    # Close the cursor and database connection.
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
