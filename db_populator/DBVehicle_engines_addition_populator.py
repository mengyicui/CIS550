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

DB_NAME = 'cis550project'

TABLES = {}

TABLES['engines_addition'] = (
    "CREATE TABLE `engines_addition` ("
    "  `engine` varchar(64) NOT NULL,"
    "  `power` int,"
    "  `torque` int,"
    "  `engine_cylinder` int,"
    "  `compression_ratio` float,"
    "  PRIMARY KEY (`engine`)"
    ")"
)

col_name = []
col_needed = ['Engine', \
                'Power (hp - kW /rpm)', 'Torque (Nm/rpm)', 'Others', \
                'Compression ratio']

_col = ['engine', 'power', 'torque', 'engine_cylinder', \
        'compression_ratio']

def make_query(_col, info):
    query = """INSERT INTO engines_addition ("""
    for i in range(0, len(_col)):
        # query += """ '""" + _col[i] + """' """
        query += _col[i]
        if i != len(_col) - 1:
            query += """, """
    query += """ ) VALUES ( """
    for i in range(0, len(info)):
        if _col[i] == 'power' or _col[i] == 'torque' \
            or _col[i] == 'engine_cylinder' \
            or _col[i] == 'compression_ratio':
            query += info[i]
        else:
            query += """ '""" + info[i] + """' """
        if i != len(info) - 1:
            query += """, """
    query += """ )"""
    return query

# Open database connection
# db = MySQLdb.connect("localhost","root","1234","project" )
# /usr/bin/mysql -h cis550-project-mysql.cnxblynrjuzi.us-west-2.rds.amazonaws.com -P 3306 -u cis550Project18 -p project
# /usr/bin/mysql -hproject.c34htetfwwf4.us-east-1.rds.amazonaws.com -P 3306 -u wuzhengx -p cis550project
db = MySQLdb.connect("project.c34htetfwwf4.us-east-1.rds.amazonaws.com","wuzhengx","11111111","cis550project" )
print "connection success"
# prepare a cursor object using cursor() method
cursor = db.cursor()
#cursor.execute("drop table engines;")

# execute SQL query using execute() method.
if _new:
    cursor.execute(TABLES['engines_addition'])

####
engine_set = set();

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
                elif col_needed[j] == 'Compression ratio':
                    if dictionary[col_needed[j]] != '?':
                        new_line.append(dictionary[col_needed[j]])
                    else:
                        new_line.append("NULL")
                elif col_needed[j] == 'Engine':
                    if dictionary[col_needed[j]] == '?':
                        new_line.append("Unkonwn")
                    else: new_line.append(dictionary[col_needed[j]])
                else:
                    if dictionary[col_needed[j]] == '?':
                        new_line.append("NULL")
                    else: new_line.append(dictionary[col_needed[j]])
            new_line[0].lower();
            if new_line[0] in engine_set:
                continue
            engine_set.add(new_line[0])
            # insert a row here
            new_query = make_query(_col, new_line)
            print i, " ", new_query
            cursor.execute(new_query)
            db.commit()
            # for testing, only insert first 100 instances
            #if i == 1000:
            #    break
        i+=1
        
# disconnect from server
print "here\n"
#cursor.execute("drop table engines;")
db.close()