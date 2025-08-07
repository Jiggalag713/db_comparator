"""Module intended to work with system entities:
creating directories, logging, etc"""
import logging
import os
import platform
from pathlib import Path

from configuration.Directories import Directories

LOGGING_LEVEL = logging.DEBUG


class SystemConfig:
    """Class intended to work with system tasks, like
     creating directories, logging, etc"""
    def __init__(self):
        self.operating_system: str = self.define_os()
        self.directories = Directories(self.operating_system)
        self.path_to_logs: str = self.directories.service_dir + 'DbComparator.log'
        self.logging_level = LOGGING_LEVEL
        self.logger: logging.Logger = self.get_logger()

    @staticmethod
    def define_os() -> str:
        """Method returns name of operating system"""
        if "Win" in platform.system():
            return "Windows"
        return "Linux"

    def get_logger(self) -> logging.Logger:
        """Method returns logger"""
        logger = logging.getLogger("db_comparator")
        logger.setLevel(level=self.logging_level)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        file_handler = logging.FileHandler(self.path_to_logs)
        file_handler.setLevel(self.logging_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.debug('File handler added successfully')
        logger.info('Logger successfully initialized')
        return logger

    def set_directory(self, path: str) -> str:
        """Method intended for checking if given directory exists.
        In case of directory not exists, method creates it."""
        if self.operating_system == "Windows":
            return path
        directory_name = (os.path.expanduser('~') + path).replace(' ', '_')
        Path(directory_name).mkdir(parents=True, exist_ok=True)
        return directory_name

    def set_dir(self, path: str):
        """Method returns path to directory where will be stored results of comparing metadata
        of databases in current run"""
        if self.operating_system == "Windows":
            divider = "\\"
        else:
            divider = "/"
        directory_name = self.directories.result_dir + divider + path + divider
        Path(directory_name).mkdir(parents=True, exist_ok=True)
        return directory_name
