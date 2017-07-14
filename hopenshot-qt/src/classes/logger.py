"""
 @file 
 @brief This file sets the default logging settings
"""

import logging
import os, sys
from logging.handlers import RotatingFileHandler
from classes import info

logging.basicConfig(
    format="%(module)12s:%(levelname)s %(message)s",
    datefmt='%H:%M:%S',
    level=logging.INFO
)

formatter = logging.Formatter('%(module)12s:%(levelname)s %(message)s')

log = logging.getLogger('OpenShot')
log.setLevel(logging.INFO)
