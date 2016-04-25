import os
import json


def get_config_dict():
    """Gets settings dictionary

    Dictionary is saved in json format in current dir
    or dir specific for OS"""
    config_dict = None
    settings_name = "settings.json"
    location = os.curdir
    try:
        with open(os.path.join(location, settings_name)) as source:
            config_dict = json.load(source)
    except IOError:
        pass
    if config_dict is None:
        raise Exception(
            'Config file "{0}" not found! Searched in local folder'
            .format(settings_name))
    return config_dict
