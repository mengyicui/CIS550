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

memo_engine = {}

TABLES['cars'] = (
    "CREATE TABLE `cars` ("
    "  `make` varchar(255) NOT NULL,"
    "  `model` varchar(255) NOT NULL,"
    "  `year` int NOT NULL,"
    "  `transmission` enum('M','A'),"
    "  `driven_wheels` enum('R','F','A'),"
    "  `doors_number` int,"
    "  `size` enum('Compact','Midsize','Large'),"
    "  `style` varchar(255),"
    "  `highway_mpg` int,"
    "  `city_mpg` int,"
    "  `popularity` int,"
    "  `msrp` int,"
    "  `engine_code` int NOT NULL,"
    "  PRIMARY KEY (`make`, `model`, `year`, `style`, `engine_code`)"
    ")"
)


TABLES['engine'] = (
    "CREATE TABLE `engine` ("
    "  `engine_fuel_type` varchar(255),"
    "  `engine_hp` int,"
    "  `engine_cylinders` int,"
    "  `engine_code` int NOT NULL,"
    "  PRIMARY KEY (`engine_code`)"
    ")"
)

col_name = []
col_needed = ['Make', 'Model', 'Year', 'Transmission Type', \
				'Driven_Wheels', 'Number of Doors','Vehicle Size', \
				'Vehicle Style', 'highway MPG', 'city mpg', \
				'Popularity', 'MSRP']

_col = ['make', 'model', 'year', 'transmission', 'driven_wheels', \
		'doors_number', 'size', 'style', 'highway_mpg', 'city_mpg', \
		'popularity', 'msrp', 'engine_code']

_engine_col = ['engine_fuel_type', 'engine_hp', 'engine_cylinders', 'engine_code']

def make_query(_col, info, db):
	if db == "cars":
		query = """INSERT INTO cars ("""
	else:
		query = """INSERT INTO engine ("""
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
			or _col[i] == 'popularity' or _col[i] == 'msrp' or _col[i] == 'engine_code':
			query += str(info[i])
		else:
			query += """ '""" + info[i] + """' """
		if i != len(info) - 1:
			query += """, """
	query += """ )"""
	return query

# Open database connection

print "Connecting to AWS RDS MYSQL Datbase..."
db = MySQLdb.connect("project.c34htetfwwf4.us-east-1.rds.amazonaws.com","wuzhengx","11111111","cis550project" )
print "Finish Connecting to Database..."
db = MySQLdb.connect("localhost","root","1234","project" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
if _new:
	cursor.execute(TABLES['cars'])
    	cursor.execute(TABLES['engine'])

print "Uploading Database..."
# open the csv file, and populate the database
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    # getting the col name, and rows
    i = 0
    engine_index = 0
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
    		

           	 #'Engine Fuel Type', \
           	 #    'Engine HP', 'Engine Cylinders'

		engine_new_query = ""

            	engine_new_line = []
            	engine_encoding = "";
            	engine_new_line.append(dictionary['Engine Fuel Type'])
            	engine_encoding += dictionary['Engine Fuel Type']
            	engine_new_line.append(dictionary['Engine HP'])
            	engine_encoding += dictionary['Engine HP']
            	engine_new_line.append(dictionary['Engine Cylinders'])
            	engine_encoding += dictionary['Engine Cylinders']

            	if engine_encoding in memo_engine.keys():
			new_line.append(memo_engine[engine_encoding])
		else:	
			memo_engine[engine_encoding] = engine_index
                	new_line.append(engine_index)
                	engine_new_line.append(engine_index);
               	 	engine_new_query = make_query(_engine_col, engine_new_line, "engine")
                	engine_index +=1
			# print engine_new_query

    		# insert a row here
    		new_query = make_query(_col, new_line, "cars")
    		# print new_query
		try:
    			cursor.execute(new_query)
    			db.commit()
                	if engine_new_query != "":
                    		cursor.execute(engine_new_query)
                    		db.commit()
		except:
			pass
    		# for testing, only insert first 100 instances
    		#if i == 1000:
    		#	break
    	i+=1
        
# disconnect from server
<<<<<<< HEAD
db.close()
print "Finished. Closing..."
=======
print "here\n"
db.close()
>>>>>>> 087afa1bc4003e3a79c2574794dfc7f0cc69b015
