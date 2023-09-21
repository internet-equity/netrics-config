#!/usr/bin/env python3

import json
import yaml

y = {}
with open("balena_devices_output_20230915.json") as f:
  j=json.load(f)
  for i in j:
    #if i['fleet']!='admin/floto' and i['fleet']!='admin/engage' and i['fleet']!='admin/poah-default':
    if i['fleet']!='admin/' and i['fleet']!='admin/engage' and i['fleet']!='admin/poah-default':
      y[i['uuid']]={"fleet": i['fleet'], "device_name":i['device_name']}

with open("database.yaml.append", "w") as f:
  yaml.dump(y, f)

