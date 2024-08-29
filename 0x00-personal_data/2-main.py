#!/usr/bin/env python3
"""
Main file
"""

import logging

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))

# Example usage of the logger.
logger = get_logger()
logger.info("name=Bob;email=bob@dylan.com;phone=123-456-7890;ssn=000-123-0000;password=bobby2019;")
