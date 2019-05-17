import os, sys, re
from collections import defaultdict

def _fail_and_exit():
    sys.exit('[ERR] Config file is not valid. Exiting program...')

def _is_valid(file_path):
    if not os.path.isfile(file_path):
        return False
    return True

def _clean(line):
    """
    Remove any unnecessary lines from the parsed file.
    E.g. Comments
    """

    return line.split(";", 1)[0]

def _is_multi_value(line):
    if (not line.startswith('"')) and (not line.endswith('"')) and ',' in line:
        return True
    return False

def _is_a_group(line):
    groupMatch = re.match(r'\[(.+)\]', line)
    return groupMatch or None

def _is_override_setting(line):
    settingMatch = re.match(r'(.+)<(.+)>\s+\=\s+(.+)', line)
    return settingMatch or None

def _is_standard_setting(line):
    settingMatch = re.match(r'(.+)\s+\=\s+(.+)', line)
    return settingMatch or None

def _set_group(config, group_obj):
    group = group_obj.group(1)
    config[group] = {}
    return group

def _set_override_setting(config, group, setting_obj, overrides):
    (setting, override, value) = (setting_obj.group(1), setting_obj.group(2), setting_obj.group(3))
    if override not in overrides:
        return
    _set_setting(config, group, setting, value)

def _set_standard_setting(config, group, setting_obj):
    (setting, value) = (setting_obj.group(1), setting_obj.group(2))
    _set_setting(config, group, setting, value)

def _set_setting(config, group, setting, value):
    if _is_multi_value(value):
        value = value.split(',')
    config[group][setting] = value

#todo Parser class?
def load_config(file_path, overrides=[]):
    if not _is_valid(file_path):
        _fail_and_exit()
    with open(file_path) as file:
        config = defaultdict(lambda: defaultdict(lambda: None))
        current_group = None
        for line in file.read().splitlines():
            line = _clean(line)
            if not line:
                continue
            matched = _is_a_group(line)
            if matched:
                current_group = _set_group(config, matched)
                continue
            # At this point, if we don't have a "group" to assign "settings" to, we assume that the config is malformed.
            if not current_group:
                _fail_and_exit()
            matched = _is_override_setting(line)
            if matched:
                _set_override_setting(config, current_group, matched, overrides)
                continue
            matched = _is_standard_setting(line)
            if matched:
                _set_standard_setting(config, current_group, matched)
                continue
            # At this point, if we can't recognize the line format, we assume that the config is malformed.
            _fail_and_exit()
        return config


if __name__ == "__main__":
  config = load_config('dummy.config', ['production', 'staging', 'ubuntu'])
  print(config)
  print(config['common']['paid_users_size_limit'])
  print(config['ftp']['name'])
  print(config['http']['params'])
  print(config['ftp']['lastname'])
