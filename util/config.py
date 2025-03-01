# encoding: utf-8

import os
import sys
sys.path.append(os.path.dirname(__file__))
import argparse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

logger.addHandler(console_handler)

#
def withDebug(b):
	if b == True:
		logger.setLevel(logging.DEBUG)
		print(f"in debug model: {b}")