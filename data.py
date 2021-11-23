# Cleaning the data
# Adding the data do db

import json
import psycopg2


def connect(db=None, user=None, password=None):
  # Initializing connection to db, which is None by default

  try:
    conn = psycopg2.connect(database=db, user=user, 
    password=password, host='127.0.0.1', port= '5432')
    conn.autocommit = True
  except (Exception, psycopg2.Error) as error:
    print("Connection not succesful: ", error)

  return conn

def sort_and_send_data(dataset, base_name, db=None, user=None, password=None):
  # Function to sort the data and send them into database according to the specification

  # Init connection and cursor
  conn = connect(db=db, user=user, password=password)
  cursor = conn.cursor()

  # Define database table items to iterate through later
  db_items = ['connection', 'name', 'description', 
              'type', 'infra_type', 
              'Cisco-IOS-XE-ethernet:channel-group', 'mtu']

  # Iterate through dataset
  for config in dataset:

    # We need to look for: 
    # name=config['name'], description=config['description'], 
    # max_frame_size=config['mtu'], config=config, 
    # port_channel_id=config[Cisco-IOS-XE-ethernet:channel-group]['name']
    
    # Initialize a list to send to db
    list_to_db = []

    # Append items from config into list according to specification
    for pos in db_items:
      
      # Check if item is in config
      if pos in config:

        # Check if current item is "name" in order to format the output
        if pos == 'name':
          list_to_db.append(base_name + str(config[pos]))

        # Check if current item is "port_channel_id" in order to format the output
        elif pos == 'Cisco-IOS-XE-ethernet:channel-group':
          var = 'Port-channel' + str(config[pos]['number'])
          cursor.execute('SELECT id FROM homework WHERE name = (%s);', (var,))
          save_id = cursor.fetchone()
          list_to_db.append(save_id)

        # Items which don't need specific formatting are simply appended to list  
        else:
          list_to_db.append(config[pos])
      # Not availabe items 
      if pos not in config:
        list_to_db.append(None)

    # Append config into index 3 as a json format
    list_to_db.insert(3, json.dumps(config))

    #Sending `list_to_db` to database
    sql = '''INSERT INTO homework  (connection, name, 
                                    description, config, type, 
                                    infra_type, port_channel_id, max_frame_size) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
    try:
      cursor.execute(sql, (*list_to_db,))
      conn.commit()
      count = cursor.rowcount
      print(count, "Record inserted successfully into table")
    except (Exception, psycopg2.Error) as error:
      print("Failed to insert record into mobile table:", error)

  # Close connection to db  
  if conn:
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")
