import json
import yaml
defaults = {}

file_path = '../../../waf_model/code-to-bestpract.yml'
with open(file_path, 'r') as file:
    best_pract = yaml.safe_load(file)

for key, value in best_pract.items():
    defaults[key] = {}
    defaults[key]['show'] = True
    defaults[key]['importance_number_of_100'] = 25
    defaults[key]['cost_number_of_100'] = 25
    defaults[key]['short-med-long'] = 'medium'

print(yaml.dump(defaults))

