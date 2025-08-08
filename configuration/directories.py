"""Module stores directory configuration"""
import datetime
import os
from pathlib import Path


class Directories:
    """Class stores implementation of directory configuration"""
    def __init__(self, operating_system):
        self.operating_system = operating_system
        self.service_dir: str = self.set_service_dir()
        self.result_dir: str = self.set_result_dir()
        self.metadata_dir: str = self.set_dir("metadata")
        self.data_dir: str = self.set_dir("data")

    def set_service_dir(self) -> str:
        """Method returns path to special db_comparator directory"""
        if self.operating_system == "Windows":
            return self.set_directory("C:\\comparator\\")
        return self.set_directory("/comparator/")

    def set_result_dir(self) -> str:
        """Method returns path to service directory,
        intended for storing results of database comparing"""
        if self.operating_system == "Windows":
            path = f"C:\\comparator\\comparation_results\\{datetime.datetime.now()}\\"
        else:
            path = f"/comparator/test_results/{datetime.datetime.now()}/"
        return self.set_directory(path)

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
        directory_name = self.result_dir + divider + path + divider
        Path(directory_name).mkdir(parents=True, exist_ok=True)
        return directory_name
