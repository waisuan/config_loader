"""
This is a custom-made config loader module.
Purpose: To parse a varying sized input config file into an in-memory object for easy access & usage during runtime.

Author: Evan Sia Wai Suan
Date created: 16/05/2019
Python Version: 3.7
"""

import os, sys, re
from config_dict import ConfigDict

def _fail_and_exit():
    sys.exit('[ERR] Config file is not valid. Exiting program...')

def _is_valid(file_path):
    if (not file_path) or (not os.path.isfile(file_path)):
        return False
    return True

def _clean(line):
    """
    Remove any unnecessary lines from the parsed file.
    (For the sake of this assignment, we're only removing comments from the config)
    """
    if not line:
        return
    return line.split(";", 1)[0]

def _is_multi_value(value):
    """
    Check to see if a value needs to be translated to a <list> type.
    Criteria: Value is not enclosed with double-quotes and is comma-delimited.
    """
    if value and (not value.startswith('"')) and (not value.endswith('"')) and ',' in value:
        return True
    return False

def _is_bool_true(value):
    return value and value.lower() in ['yes', 'true', '1']

def _is_bool_false(value):
    return value and value.lower() in ['no', 'false', '0']

def _cast(value):
    """
    Translate/convert any raw values from the parsed config into their respective data types (if possible).
    (For the sake of this assignment, we're only handling list and boolean types)
    """
    if (not value) or isinstance(value, dict) or isinstance(value, list):
        return value
    if _is_multi_value(value):
        return value.split(',')
    elif _is_bool_true(value):
        return True
    elif _is_bool_false(value):
        return False
    return value

def _is_a_group(line):
    """
    Searches and returns True if the `[group]` patten is found.
    """
    if not line:
        return
    groupMatch = re.match(r'\[(.+)\]', line)
    return groupMatch.group(1) if groupMatch else None

def _set_group(config, group):
    if (config is not None) and group and (group not in config):
        config[group] = ConfigDict()
        return True
    return False

def _is_override_setting(line):
    """
    Searches and returns True if the `setting<override> = value2` pattern is found.
    """
    if not line:
        return
    settingMatch = re.match(r'(\S+)<(\S+)>\s*\=\s*(.+)', line)
    return (settingMatch.group(1), settingMatch.group(2), settingMatch.group(3)) if settingMatch else None

def _is_standard_setting(line):
    """
    Searches and returns True if the `setting = value` pattern is found.
    """
    if not line:
        return
    settingMatch = re.match(r'(\S+)\s*\=\s*(.+)', line)
    return (settingMatch.group(1), settingMatch.group(2)) if settingMatch else None

def _set_override_setting(config, group, setting_obj, overrides):
    if (not config) or (not group) or (not setting_obj):
        return False
    (setting, override, value) = setting_obj
    if overrides and (override not in overrides):
        return True
    return _set_setting(config, group, setting, value)

def _set_standard_setting(config, group, setting_obj):
    if (not config) or (not group) or (not setting_obj):
        return False
    (setting, value) = setting_obj
    return _set_setting(config, group, setting, value)

def _set_setting(config, group, setting, value):
    if (not config) or (not group) or (not setting):
        return False
    config.append(group, setting, _cast(value))
    return True

def load_config(file_path, overrides=[]):
    if not _is_valid(file_path):
        _fail_and_exit()
    with open(file_path) as file:
        config = ConfigDict()
        current_group = None
        for line in file.read().splitlines():
            line = _clean(line)
            if not line:
                continue
            # Begin parse by looking for any "group" to init config obj with.
            # -- If not found, proceed with the last detected "group".
            current_group = _is_a_group(line) or current_group
            if _set_group(config, current_group):
                continue
            elif not current_group:
                # At this point, if we don't have a "group" to assign "settings" to, we assume that the config is malformed.
                _fail_and_exit()
            override_setting = _is_override_setting(line)
            if _set_override_setting(config, current_group, override_setting, overrides):
                continue
            standard_setting = _is_standard_setting(line)
            if _set_standard_setting(config, current_group, standard_setting):
                continue
            # At this point, if we can't recognize the line format, we assume that the config is malformed.
            _fail_and_exit()
        return config


if __name__ == "__main__":
    config = load_config('dummy.config', ['production', 'staging', 'ubuntu'])
    print(config.common.basic_size_limit)
    print(config.common.student_size_limit)
    print(config.common.paid_users_size_limit)
    print(config.common['paid_users_size_limit'])
    print(config.common.path)
    print(config.ftp.name)
    print(config.ftp['name'])
    print(config.http.params)
    print(config.ftp.lastname)
    print(config.ftp.enabled)
    print(config.ftp.path)
    print(config.ftp['path'])
    print(config.ftp)
    print(config.this.does._not_.exist)
    print(config.this['does']['not']['exist'])
 