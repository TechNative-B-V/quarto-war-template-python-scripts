import json
import yaml
import os

import lib

if "PILLAR" in os.environ:
    prios = lib.create_priority_yaml(True)
    print(yaml.dump(prios[os.environ['PILLAR']]))
else:
    prios = lib.create_priority_yaml(False)
    print(yaml.dump(prios))

## backup if allready exist
## sep files
## output only
