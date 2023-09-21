from balena import Balena
import os, sys

if os.environ['FLOTO_API_KEY'] is None:
  print("ERROR: env FLOTO_API_KEY not set.")
  sys.exit(1)

if os.environ['NETRICS_ACTIVATION_DATE'] is None:
  print("ERROR: env NETRICS_ACTIVATION_DATE not set.")
  sys.exit(1)

balena = Balena()
balena.settings.set(key="api_endpoint", value="https://api.floto.science/")
balena.settings.set(key="pine_endpoint", value="https://api.floto.science/v6/")
auth_token = os.environ['FLOTO_API_KEY']
balena.auth.login_with_token(auth_token)

devices = balena.models.device.get_all_by_application('admin/protek-il')
online_devices = {}
for device in devices:
    if device.get('api_heartbeat_state', 0) == "online":
        online_devices[device['uuid']] = device

for uuid in online_devices.keys():
    balena.models.device.env_var.set(uuid, 'NETRICS_ACTIVATION_DATE',
      os.environ['NETRICS_ACTIVATION_DATE'])

balena.auth.logout()
