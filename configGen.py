
# import os
# from configparser import ConfigParser
# config = ConfigParser()

# config.read('config.ini')
# config.add_section('main')
# config.set('main', 'default_dir1', os.path.normpath(os.path.expanduser("~/Desktop")))
# config.set('main', 'default_dir2', os.path.normpath(os.path.expanduser("~/Desktop")))

# with open('config.ini', 'w') as f:
#     config.write(f)

# DEBUGGING ONLY (don't run unless you know what you're doing)
import json
import os
import sys

config = {
    "default_dir1": os.path.normpath(os.path.expanduser("~/Desktop")),
    "default_dir2": os.path.normpath(os.path.expanduser("~/Desktop"))
          }

with open(sys.path[0] + '\\config.json', 'w') as f:
    json.dump(config, f)