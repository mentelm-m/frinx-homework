import json
from data import sort_and_send_data, create_db, create_table, database, username, password


if database == 'frinx':
    create_db()
    create_table()

create_table()

with open('configClear_v2.json', 'r') as f:
  data = json.load(f)

interfaces = data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']

for key, value in interfaces.items():
  if key == 'Port-channel':
    sort_and_send_data(value, 'Port-channel', db=database, user=username, password=password)
  if key == 'TenGigabitEthernet':
    sort_and_send_data(value, 'TenGigabitEthernet', db=database, user=username, password=password)
  elif key == 'GigabitEthernet':
    sort_and_send_data(value, 'GigabitEthernet', db=database, user=username, password=password)

  # Functionality for for BDI and Loopback - uncomment below
#   elif key == 'BDI':
#     sort_and_send_data(value, 'BDI', db=database, user=username, password=password)
#   elif key == 'Loopback':
#     sort_and_send_data(value, 'Loopback', db=database, user=username, password=password)