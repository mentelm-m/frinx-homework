# Creating a database and a table

import psycopg2
from data import connect, database, username, password

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



