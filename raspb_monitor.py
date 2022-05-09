import logging
import sys
import platform
import os
import time
import subprocess
import psutil
import socket
import uuid
import peewee

from uuid import getnode

from logging import Logger
from datetime import datetime

from monitoring.data import CPU, CPUMeasurement, Memory, MemoryMeasurement, Machine
from monitoring.config import DATABASE
from monitoring.database.db_helper import setup_db

file_dir = os.path.abspath(__file__)
par_dir = os.path.abspath(os.path.join(file_dir, os.pardir))
log_dir = os.path.join(os.path.abspath(os.path.join(os.path.join(par_dir, os.pardir))), "logs", "device_logs")


class RaspbMonitor(object):

    def __init__(self):
        logging.basicConfig(filename=f"{log_dir}/device_monitor.log", filemode="w", level=logging.DEBUG)
        self.logger = Logger(name=f"Device monitor - {datetime.now()}", level=logging.DEBUG)

        self.start_time = datetime.now()

        self.database = DATABASE

    def get_stats():

