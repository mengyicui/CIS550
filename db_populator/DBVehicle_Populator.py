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
    "  `engine` varchar(64) NOT NULL,"
    "  `power` int,"
    "  `torque` int,"
    "  `engine_cylinder` int,"
    "  `transmission` varchar(32),"
    "  `average_consumption` float,"
    "  `weight` int,"
    "  `displacement` int,"
    "  `compression_ratio` float,"
    "  `traction_type` varchar(16),"
    "  `tyre` varchar(32),"
    "  PRIMARY KEY (`make`, `model`, `engine`, `tyre`)"
    ")"
)

col_name = []
col_needed = ['Make', 'Model', 'Engine', \
                'Power (hp - kW /rpm)', 'Torque (Nm/rpm)', 'Others', 'GearBox type', \
                'Average fuel consumption (l/100 km)', 'Weight(3p/5p) kg','Displacement', \
                'Compression ratio', 'Traction type', 'Tyre']

_col = ['make', 'model', 'engine', 'power', 'torque', 'engine_cylinder', \
        'transmission', 'average_consumption', 'weight', 'displacement', \
        'compression_ratio', 'traction_type', 'tyre']

def make_query(_col, info):
    query = """INSERT INTO cars ("""
    for i in range(0, len(_col)):
        # query += """ '""" + _col[i] + """' """
        query += _col[i]
        if i != len(_col) - 1:
            query += """, """
    query += """ ) VALUES ( """
    for i in range(0, len(info)):
        if _col[i] == 'power' or _col[i] == 'torque' \
            or _col[i] == 'engine_cylinder' or _col[i] == 'weight' \
            or _col[i] == 'displacement' or _col[i] == 'compression_ratio' \
            or _col[i] == 'popularity' or _col[i] == 'average_consumption':
            query += info[i]
        else:
            query += """ '""" + info[i] + """' """
        if i != len(info) - 1:
            query += """, """
    query += """ )"""
    return query

# Open database connection
db = MySQLdb.connect("localhost","root","1234","project" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
if _new:
    cursor.execute(TABLES['cars'])

# open the csv file, and populate the database
with open('DBVehiclePTE.csv', 'rb') as f:
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
                #print col_needed[j]
                #print dictionary[col_needed[j]]
                if col_needed[j] == 'Power (hp - kW /rpm)':
                    power_raw = dictionary[col_needed[j]]
                    power_lst = power_raw.split('-')
                    if power_lst[0] == '?':
                        new_line.append("NULL")
                    else: new_line.append(power_lst[0])
                elif col_needed[j] == 'Torque (Nm/rpm)':
                    torque_raw = dictionary[col_needed[j]]
                    torque_lst = torque_raw.split('/')
                    if torque_lst[0] == '?':
                        new_line.append("NULL")
                    else: new_line.append(torque_lst[0])
                elif col_needed[j] == 'Others':
                    raw = dictionary[col_needed[j]]
                    raw_lst = raw.split('+')
                    s = raw_lst[0]
                    if s[0] == '?' or len(raw_lst) == 1:
                        new_line.append("NULL")
                    else: new_line.append(s[0:-1])
                elif col_needed[j] == 'Weight(3p/5p) kg':
                    weight_raw = dictionary[col_needed[j]]
                    weight_lst = weight_raw.split('/')
                    if weight_lst[0] == '?':
                        new_line.append("NULL")
                    else: new_line.append(weight_lst[0])
                elif col_needed[j] == 'Compression ratio':
                    if dictionary[col_needed[j]] != '?':
                        new_line.append(dictionary[col_needed[j]])
                    else:
                        new_line.append("NULL")
                elif col_needed[j] == 'engine':
                    if dictionary[col_needed[j]] == '?':
                        new_line.append("Unkonwn")
                    else: new_line.append(dictionary[col_needed[j]])
                else:
                    if dictionary[col_needed[j]] == '?':
                        new_line.append("NULL")
                    else: new_line.append(dictionary[col_needed[j]])
            
            # insert a row here
            new_query = make_query(_col, new_line)
            #print new_query
            #print "\n"
            cursor.execute(new_query)
            db.commit()
            # for testing, only insert first 100 instances
            #if i == 1000:
            #    break
        i+=1
        
# disconnect from server
print "here\n"
db.close()