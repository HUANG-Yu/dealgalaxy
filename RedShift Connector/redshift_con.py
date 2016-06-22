import psycopg2
import sys
import pprint
from datetime import date, timedelta

#Connect to RedShift

conn = psycopg2.connect(conn_string);

cursor = conn.cursor();

#Captures Column Names 
column_names = [];
cursor.execute("Select * from item limit 10;");
column_names = [desc[0] for desc in cursor.description]
all_cols=', '.join([str(x) for x in column_names])
print all_cols;

conn.commit();
conn.close();