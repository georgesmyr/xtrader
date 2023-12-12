from pathlib import Path
import sys
import toml
import json

from collections.abc import Mapping
from typing import Union, Optional, Tuple
from os import PathLike


class SparkConnect:

    def __init__(self, host: str,
                 token: str,
                 cluster_id: str,
                 org_id: int,
                 port: int = 15001,
                 root_dir: Optional[str] = None,
                 **kwargs):
        """
        Initializes spark session from configuration parameters and key-word arguments.
        :param host:
        :param token:
        :param cluster_id:
        :param org_id:
        :param port:
        :param root_dir: ingestion layer
        """
        self._config = {"databricks_connect": {"host": host,
                                               "token": token,
                                               "cluster_id": cluster_id,
                                               "org_id": org_id,
                                               "port": port},
                        "root_dir": root_dir
                        }
        # Merge any kwargs to config
        self._config = SparkConnect._merge_config_dicts(self._config, kwargs)
        # Set spark session and dbutils to None
        self._spark, self._dbutils = None, None

    @classmethod
    def from_config(cls,
                  file: Optional[Union[PathLike, str]] = "config.toml",
                  **kwargs):
        """
        Initializes a new session
        :param file: The name of the configuration file to load
        """
        # Parse all config files and parameters.
        config = {}
        # Find and load the general config. Merge it with config
        config_file, config_path = SparkConnect._load_config(file)
        # Merge in config_file to the config
        config = SparkConnect._merge_config_dicts(config, config_file)
        # Merge in any kwargs to the config
        config = SparkConnect._merge_config_dicts(config, kwargs)

        # If the toml config file contains a location of Databricks-Connect json config file
        if "databricks_connect" in config and "config_file" in config["databricks_connect"]:
            databricks_config_path = Path(config["databricks_connect"]["config_file"]).expanduser()
            if databricks_config_path.exists():
                with open(databricks_config_path, "r") as dbfile:
                    config["databricks_connect"] = SparkConnect._merge_config_dicts(
                        config["databricks_connect"], json.load(dbfile), overwrite=False,
                    )

        dbconnect_params = config["databricks_connect"]
        kw_args = {key: value for key, value in config.items() if key != "databricks_connect"}

        return cls(**dbconnect_params, **kw_args)

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
                ).getOrCreate()
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

    def get_spark_session(self):
        """ Returns spark session """
        return self.spark

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

    def get_dbutils(self):
        """ Gets dbutils """
        return self.dbutils
    
    @staticmethod
    def _load_config(filename: str) -> Tuple[Mapping, PathLike]:
        """
        Loads a configuration file from a TOML or JSON file.

        :param filename: Filename or path to the configuration file
        :return: A dictionary containing the configuration
        """
        if filename is None:
            raise ValueError("No configuration file was specified")
        
        config_path = SparkConnect._find_config_path(filename)
        if config_path is None:
            raise FileNotFoundError(f"Could not find configuration file '{filename}'")
        
        # Load the configuration file
        if filename.endswith(".json"):
            with open(config_path, "r") as json_file:
                config_file = json.load(json_file)
        elif filename.endswith(".toml"):
            config_file = toml.load(config_path)

        return config_file, config_path

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
        the overwrite parameter is set to False.

        :param current: The current configuration dictionary
        :param update: The update configuration dictionary
        :param overwrite: Whether to overwrite keys from 'update' to 'current'
        :return: A merged version of the `current` and `update` dictionaries
        """
        for key, value in update.items():
            if key in current:
                if isinstance(current[key], Mapping) and isinstance(value, Mapping):
                    current[key] = SparkConnect._merge_config_dicts(current[key], value)
                elif overwrite:
                    current[key] = value
            else:
                current[key] = value

        return current
    

def main():

    connections = SparkConnect.from_config("config.json")
    print(connections.__dict__)


if __name__ == "__main__":
    main()