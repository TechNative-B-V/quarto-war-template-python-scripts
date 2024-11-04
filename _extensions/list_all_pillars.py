import json
import yaml

import lib

lib.create_priority_yaml()

print(yaml.dump(lib.allPillars))
