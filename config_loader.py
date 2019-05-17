import os, sys, re


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

def _matchForGroups(line):
    groupMatch = re.match(r'\[(.+)\]', line)
    if groupMatch:
        return groupMatch.group(1)
    return None

def _matchForOverrideSettings(line, overrides):
    settingMatch = re.match(r'(.+)<(.+)>\s+\=\s+(.+)', line)
    if settingMatch:
        (setting, override, value) = (settingMatch.group(1), settingMatch.group(2), settingMatch.group(3))
        if override not in overrides:
            return None
        return { 'key': setting, 'value': value }
    return None

def _matchForStandardSettings(line):
    settingMatch = re.match(r'(.+)\s+\=\s+(.+)', line)
    if settingMatch:
        (setting, value) = (settingMatch.group(1), settingMatch.group(2))
        if _is_multi_value(value):
            value = value.split(',')
        return { 'key': setting, 'value': value }
    return None

#todo Parser class?
def load_config(file_path, overrides=[]):
    if not _is_valid(file_path):
        sys.exit('[ERR] Config file is not valid. Exiting program...')
    with open(file_path) as file:
        config = {}
        current_group = ''
        for line in file.read().splitlines():
            line = _clean(line)
            if not line:
                continue
            group = _matchForGroups(line)
            if group:
                current_group = group
                continue
            override_setting = _matchForOverrideSettings(line, overrides)
            if override_setting:
                #config[current_group][override_setting['key']] = override_setting['value']
                continue
            std_setting = _matchForStandardSettings(line)
            if std_setting:
                config[current_group] = std_setting
                #config[current_group][std_setting['key']] = std_setting['value']
                continue
            #todo
            sys.exit('[ERR] Config file is not valid. Exiting program...')
        print(config)


if __name__ == "__main__":
  load_config('dummy.config')
