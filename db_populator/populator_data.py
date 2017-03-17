#####################################
# 1. Install mysql
# 2. Start an instance
# 3. Python connect to localhost:3306
# 4. Create tables and populate

# Arthur:
# Zhengxuan Wu, Fengkai Wu, Mengyi Cui
# University Of Pennsylvania
#####################################

import MySQLdb
import csv

_new = 1;

DB_NAME = 'project'

TABLES = {}

TABLES['cars'] = (
    "CREATE TABLE `cars` ("
    "  `make` varchar(255) NOT NULL,"
    "  `model` varchar(255) NOT NULL,"
    "  `year` int NOT NULL,"
    "  `engine_fuel_type` varchar(255),"
    "  `engine_hp` int,"
    "  `engine_cylinders` int,"
    "  `transmission` enum('M','A'),"
    "  `driven_wheels` enum('R','F','A'),"
    "  `doors_number` int,"
    "  `size` enum('Compact','Midsize','Large'),"
    "  `style` varchar(255),"
    "  `highway_mpg` int,"
    "  `city_mpg` int,"
    "  `popularity` int,"
    "  `msrp` int,"
    "  PRIMARY KEY (`make`, `model`, `year`, `style`, `engine_hp`)"
    ")"
)

col_name = []
col_needed = ['Make', 'Model', 'Year', 'Engine Fuel Type', \
				'Engine HP', 'Engine Cylinders', 'Transmission Type', \
				'Driven_Wheels', 'Number of Doors','Vehicle Size', \
				'Vehicle Style', 'highway MPG', 'city mpg', \
				'Popularity', 'MSRP']

_col = ['make', 'model', 'year', 'engine_fuel_type', 'engine_hp', \
		'engine_cylinders', 'transmission', 'driven_wheels', \
		'doors_number', 'size', 'style', 'highway_mpg', 'city_mpg', \
		'popularity', 'msrp']

def make_query(_col, info):
	query = """INSERT INTO cars ("""
	for i in range(0, len(_col)):
		# query += """ '""" + _col[i] + """' """
		query += _col[i]
		if i != len(_col) - 1:
			query += """, """
	query += """ ) VALUES ( """
	for i in range(0, len(info)):
		if _col[i] == 'year' or _col[i] == 'engine_hp' \
			or _col[i] == 'engine_cylinders' or _col[i] == 'doors_number' \
			or _col[i] == 'highway_mpg' or _col[i] == 'city_mpg' \
			or _col[i] == 'popularity' or _col[i] == 'msrp':
			query += info[i]
		else:
			query += """ '""" + info[i] + """' """
		if i != len(info) - 1:
			query += """, """
	query += """ )"""
	return query

# Open database connection
db = MySQLdb.connect("localhost","root","1111","project" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
if _new:
	cursor.execute(TABLES['cars'])

# open the csv file, and populate the database
with open('data.csv', 'rb') as f:
    reader = csv.reader(f)
    # getting the col name, and rows
    i = 0
    for row in reader:
    	if i == 0:
    		col_name = row
    	else:
    		dictionary = dict(zip(col_name, row))
    		new_line = []
    		for j in range(0, len(col_needed)):
    			if col_needed[j] == 'Market Category':
    				continue
    			elif col_needed[j] == 'Transmission Type':
    				new_line.append(dictionary[col_needed[j]][0])
    			elif col_needed[j] == 'Driven_Wheels':
    				new_line.append(dictionary[col_needed[j]].upper()[0])
    			else:
    				new_line.append(dictionary[col_needed[j]])
    		
    		# insert a row here
    		new_query = make_query(_col, new_line)
    		print new_query
    		cursor.execute(new_query)
    		db.commit()
    		# for testing, only insert first 100 instances
    		if i == 5:
    			break
    	i+=1
        
# disconnect from server
db.close()