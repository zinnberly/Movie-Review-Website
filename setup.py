# Sam Zinn
# sjz20g
# due 02/21/24
# The program in this file is the individual work of Sam Zinn

import sqlite3

conn = sqlite3.connect('movieData.db')
print ('Opened database successfully')

conn.execute('CREATE TABLE Reviews (Username TEXT, MovieID TEXT, ReviewTime DATETIME, Rating FLOAT, Review TEXT)')
print('Created Review table')
conn.execute('CREATE TABLE Movies (MovieID TEXT PRIMARY KEY, Title TEXT, Director TEXT, Genre TEXT, Year INTEGER)')
print('Created Movie table')

conn.close()
