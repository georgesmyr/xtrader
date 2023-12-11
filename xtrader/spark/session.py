from pathlib import Path
import sys
import toml

# Typing 
import collections.abc
from typing import Union, Optional, Tuple
from os import PathLike

class Session:


    def __init__(self,
                 config_file: Union[PathLike, str] = "config.toml",
                 local_config_file: Union[PathLike, str] = "config.local.toml",
                 **kwargs):
        """
        Initializes a new session

        :param config_file: The name of the configuration file to load
        :param local_config_file: The name of the local configuration file to load
        """
        # Parse all config files and parameters.
        self._config = {}
        # Find and load the general config. Merge it with config
        self._config, self._config_path = Session._merge_config(self._config, config_file)
        # Find and load the local config. Merge it with config
        self._config, self._local_config_path = Session._merge_config(self._config, local_config_file)
        # Merge in any kwargs to the config
        self._config = Session._merge_config_dicts(self._config, kwargs)


    @staticmethod
    def _merge_config(current: collections.abc.Mapping, file: Union[PathLike, str]) -> Tuple[dict, str]:
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
        Otherwise, if the file is a relative path then this method will check if the file exists in the current working directory
        (and all subdirectories) as well as on the system path(s).

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
    def _merge_config_dicts(current: collections.abc.Mapping, update: collections.abc.Mapping, overwrite: bool = True):
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
                if isinstance(current[key], collections.abc.Mapping) and isinstance(value, collections.abc.Mapping):
                    current[key] = Session._merge_config(current[key], value)
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