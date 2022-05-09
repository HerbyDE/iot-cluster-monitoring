import logging
import sys
import platform
import os
import time
import subprocess
import psutil
import socket
import uuid

from uuid import getnode

from logging import Logger
from datetime import datetime
import peewee

from monitoring.data import CPU, CPUMeasurement, Memory, MemoryMeasurement, Machine
from monitoring.config import DATABASE
from monitoring.database.db_helper import setup_db

file_dir = os.path.abspath(__file__)
par_dir = os.path.abspath(os.path.join(file_dir, os.pardir))
log_dir = os.path.join(os.path.abspath(os.path.join(os.path.join(par_dir, os.pardir))), "logs", "device_logs")


class DeviceMonitor(object):
    """
    This device monitor stores all essential metrics in a PostgreSQL database. Included components: CPU, Memory
    TODO: Include temperature & disk features.
    """

    def __init__(self):

        logging.basicConfig(filename=f"{log_dir}/device_monitor.log", filemode="w", level=logging.DEBUG)
        self.logger = Logger(name=f"Device monitor - {datetime.now()}", level=logging.DEBUG)

        self.start_time = datetime.now()

        # The device monitor instantiates a local database to store metrics. Once monitoring is done, the data will be
        # sent to a MQTT broker.
        # TODO: Create Ansible script to introduce monitoring service and and configure PostgreSQL db
        self.database = DATABASE

    def setup(self) -> None:
        setup_db([CPU, CPUMeasurement, Memory, MemoryMeasurement, Machine], database=self.database)
        self.mac_address = hex(uuid.getnode())[2:]

        # Setup the machine model in database
        machine_data = {
            "name": f"{platform.uname()[1]}",  # Prints the node name
            "ip": socket.gethostbyname(socket.gethostname()),
            "mac_addr": self.mac_address,  # This is the primary key for ForeignKeys
            "device_architecture": platform.machine(),
            "operating_system": platform.system(),
            "timestamp": datetime.now(),
            "device_class": platform.platform(),
            "storage": psutil.disk_usage('/').total
        }
        self.machine, created_mac = Machine.get_or_create(mac_addr=self.mac_address, defaults=machine_data)

        # setup the cpu model in database (make sure to keep the CPU primary key available)
        cpu_data = {
            "machine": self.mac_address,
            "name": platform.processor(),
            "cores": psutil.cpu_count(logical=False),
            "min_freq": psutil.cpu_freq()[1],
            "max_freq": psutil.cpu_freq()[2]
        }
        self.cpu, created_cpu = CPU.get_or_create(machine=self.mac_address, defaults=cpu_data)

        # Setup the memory model in database (make sure to keep memory primary key available)
        memory_data = {
            "machine": self.mac_address,
            "total": psutil.virtual_memory()[0],
            "total_swap": psutil.swap_memory()[0],
            "comments": ""
        }
        self.memory, created_mem = Memory.get_or_create(machine=self.mac_address, defaults=memory_data)

    def collect_metrics(self, mps=1, start_time=None, end_after=None) -> None:
        """
        Collects all device metrics from CPU, Memory, and Swap.
        If no end after is specified, the measurement will end after 24h.
        :param mps:                         Measurements per second
        :param start_time:                  Datetime object specifying the start time. If none, starts immediately.
        :param end_after:                   Either int (number of measurements) or a datetime object.
        :return: None
        """

        if start_time:
            delta = start_time - datetime.now()
            time.sleep(delta.seconds)

        self.start_time = datetime.now()
        loop = 0

        while True:
            timestamp = datetime.now()
            cpu = self.get_cpu_measurement()
            memory = self.get_memory_and_swap_measurement()

            self.generate_cpu_record(data=cpu, timestamp=timestamp)
            self.generate_memory_record(data=memory, timestamp=timestamp)

            time.sleep(1/mps)
            loop += 1

            if end_after:
                if type(end_after) == datetime:
                    if datetime.now() == end_after:
                        break
                elif type(end_after) == int:
                    if loop == end_after:
                        break
                else:
                    raise NotImplementedError("There is no break condition for the data type you specified.")

    def get_cpu_measurement(self) -> dict:
        cpu_metrics = psutil.cpu_times_percent(percpu=True)
        cpu_data = {
            "user": list(),
            "nice": list(),
            "system": list(),
            "idle": list(),
            "freq": list(),
        }

        for cpu in cpu_metrics:
            cpu_data["user"].append(cpu.user)
            cpu_data["nice"].append(cpu.nice)
            cpu_data["system"].append(cpu.system)
            cpu_data["idle"].append(cpu.idle)

        cpu_freqs = psutil.cpu_freq(percpu=True)

        for cpu in cpu_freqs:
            cpu_data["freq"].append(cpu.current)

        return cpu_data

    def get_memory_and_swap_measurement(self) -> dict:
        """
        Obtains memory values from the system.

        Average execution time after 10.000 runs with time.time() is
        3.42e-05 s.

        :return: dict, memory values
        """
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        data = dict()

        data["used"] = memory.used
        data["free"] = memory.free
        data["wired"] = memory.wired
        data["available"] = memory.available
        data["utilization"] = memory.percent
        data["swap_used"] = swap.used
        data["swap_free"] = swap.free

        return data

    def generate_cpu_record(self, data: dict, timestamp=datetime.now()) -> None:
        """
        Takes a dict writes it off to a database
        :param data: Dict with all attributes
        :return: None
        """
        assert type(data) == dict
        for k, v in data.items():
            data[k] = str(v)

        rec = CPUMeasurement(**data)
        rec.cpu = self.cpu._pk
        rec.timestamp = timestamp
        rec.save(force_insert=True)

    def generate_memory_record(self, data: dict, timestamp=datetime.now()) -> None:
        """
        Takes a dict writes it off to a database
        :param data: Dict with all attributes
        :param timestamp: Timestamp to include in the record
        :return: None
        """
        assert type(data) == dict

        rec = MemoryMeasurement(**data)
        rec.memory = self.memory._pk
        rec.timestamp = timestamp
        rec.save(force_insert=True)


#############################################################
#                Part that launches the service             #
#############################################################
if __name__ == "__main__":
    monitor = DeviceMonitor()
    monitor.setup()
    monitor.collect_metrics(mps=1)





