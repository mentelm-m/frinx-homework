# Cleaning the data
# Adding the data do db

import json
import psycopg2
from getpass import getpass

database = input("Choose a database: ")
username = input("Choose a user: ")
password = getpass("Enter valid password: ")

def connect(db=None, user=username, password=password):
  # Initializing connection to db, which is None by default

  try:
    conn = psycopg2.connect(database=db, user=user, 
    password=password, host='127.0.0.1', port= '5432')
    conn.autocommit = True
  except (Exception, psycopg2.Error) as error:
    print("Connection not succesful: ", error)

  return conn

def sort_and_send_data(dataset, base_name, db=database, user=username, password=password):
  # Function to sort the data and send them into database according to the specification
  max_list = []
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
    max_list.append(list_to_db)

    # Setup SQL command for execution
    sql = '''INSERT INTO homework  (connection, name, 
                                    description, config, type, 
                                    infra_type, port_channel_id, max_frame_size) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
  
  # Sending `max_list` to database
  try:
    cursor.executemany(sql, (*max_list,))
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


def create_db():
  # Init connection to server, creating new database `frinx`
  if database == 'frinx':
    try:
      conn = connect(user=username, password=password)
      cursor = conn.cursor()
      cursor.execute('CREATE DATABASE frinx;')
      conn.commit()
    except (Exception, psycopg2.Error) as error:
      print("Error creating a database: ", error)

    # Close the connection
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")


def create_table():
  # Re-init connection to server and new database
  try:
    conn = connect(db=database, user=username, password=password)
    cursor = conn.cursor()
  except (Exception, psycopg2.Error) as error:
    print("Error initializing connection: ", error)

  # Defining table model according to specification
  sql ='''CREATE TABLE IF NOT EXISTS homework (
    id SERIAL PRIMARY KEY,
    connection INTEGER,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    config json,
    type VARCHAR(50),
    infra_type VARCHAR(50),
    port_channel_id INTEGER,
    max_frame_size INTEGER
  );'''
  cursor.execute(sql)

  # Close the connection
  if conn:
      cursor.close()
      conn.close()
      print("PostgreSQL connection is closed")
