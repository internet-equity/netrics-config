#!/usr/bin/env python3

import json
import yaml

y = {}
with open("balena_devices_output.json") as f:
  j=json.load(f)
  for i in j:
    if i['fleet']=='admin/poah-staging':
       y[i['uuid']]={"fleet": i['fleet']}

with open("database.yaml.append", "w") as f:
  yaml.dump(y, f)

