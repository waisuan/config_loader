import os, sys, re

class Config:
    def __init__(self):
        self.config = {}

    def __fail_and_exit(self):
        sys.exit('[ERR] Config file is not valid. Exiting program...')

    def __is_valid(self, file_path):
        if not os.path.isfile(file_path):
            return False
        return True

    def __clean(self, line):
        """
        Remove any unnecessary lines from the parsed file.
        E.g. Comments
        """

        return line.split(";", 1)[0]

    def __is_multi_value(self, line):
        if (not line.startswith('"')) and (not line.endswith('"')) and ',' in line:
            return True
        return False

    def __is_a_group(self, line):
        groupMatch = re.match(r'\[(.+)\]', line)
        return groupMatch or None

    def __is_override_setting(self, line):
        settingMatch = re.match(r'(.+)<(.+)>\s+\=\s+(.+)', line)
        return settingMatch or None

    def __is_standard_setting(self, line):
        settingMatch = re.match(r'(.+)\s+\=\s+(.+)', line)
        return settingMatch or None

    def __set_group(self, group_obj):
        group = group_obj.group(1)
        self.config[group] = {}
        return group

    def __set_override_setting(self, group, setting_obj, overrides):
        (setting, override, value) = (setting_obj.group(1), setting_obj.group(2), setting_obj.group(3))
        if override not in overrides:
            return
        self.__set_setting(group, setting, value)

    def __set_standard_setting(self, group, setting_obj):
        (setting, value) = (setting_obj.group(1), setting_obj.group(2))
        self.__set_setting(group, setting, value)

    def __set_setting(self, group, setting, value):
        if self.__is_multi_value(value):
                value = value.split(',')
        self.config[group][setting] = value

    #todo Parser class?
    def load_config(self, file_path, overrides=[]):
        if not self.__is_valid(file_path):
            self.__fail_and_exit()
        with open(file_path) as file:
            current_group = None
            for line in file.read().splitlines():
                line = self.__clean(line)
                if not line:
                    continue
                matched = self.__is_a_group(line)
                if matched:
                    current_group = self.__set_group(matched)
                    continue
                if not current_group:
                    self.__fail_and_exit()
                matched = self.__is_override_setting(line)
                if matched:
                    self.__set_override_setting(current_group, matched, overrides)
                    continue
                matched = self.__is_standard_setting(line)
                if matched:
                    self.__set_standard_setting(current_group, matched)
                    continue
                self.__fail_and_exit()
            return self.config


if __name__ == "__main__":
  config = Config()
  CONFIG = config.load_config('dummy.config', ['production', 'staging'])
  print(CONFIG)
