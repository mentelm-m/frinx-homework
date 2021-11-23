import json
from data import sort_and_send_data

with open('configClear_v2.json', 'r') as f:
  data = json.load(f)

interfaces = data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']

for key, value in interfaces.items():
  if key == 'Port-channel':
    sort_and_send_data(value, 'Port-channel', db='frinx', user='postgres', password='Michal31#!')
  if key == 'TenGigabitEthernet':
    sort_and_send_data(value, 'TenGigabitEthernet', db='frinx', user='postgres', password='Michal31#!')
  elif key == 'GigabitEthernet':
    sort_and_send_data(value, 'GigabitEthernet', db='frinx', user='postgres', password='Michal31#!')
  # elif key == 'BDI':
  #   sort_and_send_data(value, 'BDI', db='frinx', user='postgres', password='Michal31#!')
  # elif key == 'Loopback':
  #   sort_and_send_data(value, 'Loopback', db='frinx', user='postgres', password='Michal31#!')