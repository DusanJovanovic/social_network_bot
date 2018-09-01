import json
import os

folder = os.path.dirname(os.path.abspath(__file__))

with open(folder + '/config.json') as f:
    conf = json.load(f)

clearbit_token = conf['clearbit_token']
hunter_token = conf['hunter_token']