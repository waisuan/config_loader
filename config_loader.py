import os, sys, re

# class Config:
#     def __init__(self):
#         pass

def _is_valid(file_path):
    if not os.path.isfile(file_path):
        return False
    return True

#todo Parser class?
def _parse(file_path):
    with open(file_path) as file:
        config = {}
        for line in file.read().splitlines():
            groupMatch = re.match(r'\[(.+)\]', line)
            if groupMatch:
                print(groupMatch.group(1))
            settingMatch = re.match(r'(.+)\s+\=\s+(.+)', line)
            if settingMatch:
                print(settingMatch.group(1) + ', ' + settingMatch.group(2))
            

def load_config(file_path, overrides=[]):
    if not _is_valid(file_path):
        sys.exit("[ERR] Config file is not valid. Exiting program...")
    return _parse(file_path)


if __name__ == "__main__":
  load_config('dummy.config')
