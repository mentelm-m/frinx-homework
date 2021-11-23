# Creating a database, a table and connecting to db

from data import connect

# Init connection to server, creating new database
conn = connect()
cursor = conn.cursor()
cursor.execute('CREATE DATABASE frinx;')

# Close the connection
if conn:
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")

# Re-init connection to server and new database
conn = connect(db='frinx')
cursor = conn.cursor()

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



