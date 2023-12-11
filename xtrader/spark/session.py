from pathlib import Path
import sys
import toml
import json

from collections.abc import Mapping
from typing import Union, Optional, Tuple
from os import PathLike


class Session:

    def __init__(self,
                 config_file: Optional[Union[PathLike, str]] = "config.toml",
                 **kwargs):
        """
        Initializes a new session
        :param config_file: The name of the configuration file to load
        """
        # Parse all config files and parameters.
        self._config = {}
        # Find and load the general config. Merge it with config
        self._config, self._config_path = Session._merge_configs(self._config, config_file)
        # Merge in any kwargs to the config
        self._config = Session._merge_config_dicts(self._config, kwargs)

        # Read Databricks Connect configuration from json file if it exists
        if "databricks_connect" in self._config and "config_file" in self._config["databricks_connect"]:
            self._databricks_config_path = Path(self._config["databricks_connect"]["config_file"]).expanduser()
            if self._databricks_config_path.exists():
                with open(self._databricks_config_path, "r") as dbfile:
                    self._config["databricks_connect"] = Session._merge_config_dicts(
                        self._config["databricks_connect"], json.load(dbfile), overwrite=False,
                    )
        else:
            self._databricks_config_path = None

        # Initialize spark and dbutils to None
        self._spark = None
        self._dbutils = None

    def _init_spark(self) -> None:
        """
        Initializes spark session. If there is no active session, it creates
        a new session from loaded configuration.
        """
        from pyspark.sql import SparkSession
        if SparkSession.getActiveSession() is not None:
            self._spark = SparkSession.getActiveSession()
        elif "databricks_connect" in self._config:
            self._spark = (
                SparkSession.builder.config(
                    "spark.databricks.service.address",
                    self._config["databricks_connect"]["host"],
                )
                .config(
                    "spark.databricks.service.clusterId",
                    self._config["databricks_connect"]["cluster_id"],
                )
                .config(
                    "spark.databricks.service.token",
                    self._config["databricks_connect"]["token"],
                )
                .config(
                    "spark.databricks.service.orgId",
                    self._config["databricks_connect"]["org_id"],
                )
                .config(
                    "spark.databricks.service.port",
                    self._config["databricks_connect"]["port"],
                )
            )
        else:
            raise ValueError("No active Spark session exists and no databricks connect configuration was present.")
        
    @property
    def spark(self): #-> SparkSession
        """
        Gets the active SparkSession. If no session exists, it creates a new session.
        :return: The active SparkSession object
        """
        if self._spark is None:
            self._init_spark()
        return self._spark
    
    def _init_dbutils(self) -> None:
        """ Initializes databricks utilities dbutils """
        from pyspark.dbutils import DBUtils
        self._dbutils = DBUtils(self.spark)

    @property
    def dbutils(self): #-> DBUtils
        """
        Gets the active dbutils. If no dbutils exists, it creates a new dbutils object.
        :return: The active dbutils object
        """
        if self._dbutils is None:
            self._init_dbutils()
        return self._dbutils 

    @staticmethod
    def _merge_configs(current: Mapping, file: Union[PathLike, str]) -> Tuple[Mapping, Optional[PathLike]]:
        """
        Finds the path of the configuration file and merges it with the current configuration.
        If the file is None, then the current configuration is returned.

        :param current: The current configuration dictionary
        :param file: Filename or path to the configuration file
        :return: A merged version of the `current` and `file`, as well as the path to the configuration file
        """
        if file is not None:
            config_path = Session._find_config_path(file)
            if config_path is None:
                raise FileNotFoundError(f"Could not find configuration file '{file}'")
            else:
                return Session._merge_config_dicts(current, toml.load(config_path)), config_path
        else:
            return current, None

    @staticmethod
    def _find_config_path(file: Union[PathLike, str]) -> Optional[PathLike]:
        """
        Finds the full path of a configuration file.

        If the file is already an absolute path then this method will only check if the file exists.
        Otherwise, if the file is a relative path then this method will check if the file exists in the current
        working directory (and all subdirectories) as well as on the system path(s).

        :param file: Filename or path to the configuration file
        :return: An absolute path to the filename, or None if it cannot be found.
        """
        file = Path(file)
        if file.is_absolute():
            # For an absolute file, check if it exists
            if file.exists():
                return file
            else:
                return None
        else:
            # For a relative file, search for it and return None when it cannot be found
            search_dirs = [Path.cwd()] + list(Path.cwd().parents) + [Path(p) for p in sys.path]
            for directory in search_dirs:
                candidate_dir = directory / file
                if candidate_dir.exists():
                    return candidate_dir
            return None
        
    @staticmethod
    def _merge_config_dicts(current: Mapping, update: Mapping, overwrite: bool = True) -> Mapping:
        """
        Merges two dictionaries recursively. This will overwrite keys from 'update' to 'current' unless
        the ovewrite parameter is set to False.

        :param current: The current configuration dictionary
        :param update: The update configuration dictionary
        :param overwrite: Whether to overwrite keys from 'update' to 'current'
        :return: A merged version of the `current` and `update` dictionaries
        """
        for key, value in update.items():
            if key in current:
                if isinstance(current[key], Mapping) and isinstance(value, Mapping):
                    current[key] = Session._merge_config_dicts(current[key], value)
                elif overwrite:
                    current[key] = value
            else:
                current[key] = value
        return current


def main():
    s = Session(config_file=None, local_config_file=None, a=1, b=2, c=3)
    print(s._config)
    print(s._config_path)
    print(s._local_config_path)

if __name__ == "__main__":
    main()