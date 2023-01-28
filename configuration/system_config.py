"""Module intended to work with system entities:
creating directories, logging, etc"""
import logging
import os
import platform
from pathlib import Path

LOGGING_LEVEL = logging.DEBUG


class SystemConfig:
    """Class intended to work with system tasks, like
     creating directories, logging, etc"""
    def __init__(self):
        self.operating_system: str = self.define_os()
        self.service_dir: str = self.set_service_dir()
        self.test_dir: str = self.set_test_dir()
        self.path_to_logs: str = self.service_dir + 'DbComparator.log'
        self.logging_level = LOGGING_LEVEL
        self.logger: logging.Logger = self.get_logger()

    def set_service_dir(self) -> str:
        """Method returns path to special db_comparator directory"""
        return self.set_directory("C:\\comparator\\", "/comparator/")

    def set_test_dir(self) -> str:
        """Method returns path to service directory,
        intended for storing results of database comparing"""
        return self.set_directory("C:\\comparator\\test_results\\", "/comparator/test_results/")

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
        file_handler = logging.FileHandler(self.service_dir + 'dbcomparator.log')
        file_handler.setLevel(self.logging_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.debug('File handler added successfully')
        logger.info('Logger successfully initialized')
        return logger

    def set_directory(self, win_path: str, linux_path: str) -> str:
        """Method intended for checking if given directory exists.
        In case of directory not exists, method creates it."""
        if self.operating_system == "Windows":
            # TODO: [improve] add creation of directory below
            # TODO: [improve] check if disk C:/ is not exist
            return win_path
        directory_name = os.path.expanduser('~') + linux_path
        Path(directory_name).mkdir(parents=True, exist_ok=True)
        return directory_name
