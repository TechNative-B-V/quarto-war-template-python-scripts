import json
import yaml

pract_best = {}

file_path = '../../waf_model/code-to-bestpract.yml'
with open(file_path, 'r') as file:
    best_pract = yaml.safe_load(file)

for key, value in best_pract.items():
    pract_best[value] = key

print(yaml.dump(pract_best))

