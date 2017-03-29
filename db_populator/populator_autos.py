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

DB_NAME = 'CIS550'

TABLES = {}

TABLES['used_cars_info'] = (
    "CREATE TABLE `used_cars_info` ("
    "  `seller` varchar(255),"
    "  `price` int NOT NULL,"
    "  `vehicle_type` varchar(255),"
    "  `year_of_registration` int,"
    "  `month_of_registration` int,"
    "  `gearbox` varchar(255) NOT NULL,"
    "  `powerPS` int NOT NULL,"
    "  `vehicle_model` varchar(255) NOT NULL,"
    "  `kilometer` int,"
    "  `fuel_type` varchar(255),"
    "  `vehicle_brand` varchar(255) NOT NULL,"
    "  `postal_code` int,"
    "  PRIMARY KEY (`year_of_registration`, `month_of_registration`, `vehicle_model`, `vehicle_brand`, `powerPS`, `price`)"
    ")"
)

col_name = []
col_needed = ['seller', 'price', 'vehicleType', 'yearOfRegistration', \
                'monthOfRegistration', 'gearbox', 'powerPS', \
                 'model', 'kilometer', 'fuelType', 'brand', 'postalCode']

_col = ['seller', 'price', 'vehicle_type', \
        'year_of_registration', 'month_of_registration', 'gearbox', \
        'powerPS', 'vehicle_model', 'kilometer', \
        'fuel_type', 'vehicle_brand', 'postal_code']

def make_query(_col, info):
    query = """INSERT INTO used_cars_info ("""
    for i in range(0, len(_col)):
        # query += """ '""" + _col[i] + """' """
        query += _col[i]
        if i != len(_col) - 1:
            query += """, """
    query += """ ) VALUES ( """
    for i in range(0, len(info)):
        if _col[i] == 'price' or _col[i] == 'year_of_registration' \
            or _col[i] == 'month_of_registration' or _col[i] == 'powerPS' \
            or _col[i] == 'kilometer' or _col[i] == 'postal_code':
            query += info[i]
        else:
            query += """ '""" + info[i] + """' """
        if i != len(info) - 1:
            query += """, """
    query += """ )"""
    return query


# Open database connection
# db = MySQLdb.connect("localhost", "root", "(CUImengyi)120", "project")
db = MySQLdb.connect("project.c34htetfwwf4.us-east-1.rds.amazonaws.com", "wuzhengx", "11111111", "cis550project")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
if _new:
    cursor.execute(TABLES['used_cars_info'])

# open the csv file, and populate the database
with open('autos.csv', 'rb') as f:
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
            # insert a row here
                if col_needed[j] == 'gearbox':
                    gear = dictionary[col_needed[j]]
                    if gear == 'manuell':
                        new_line.append('M')
                    elif gear == 'automatik':
                        new_line.append('A')
                    else:
                        new_line.append('')
                elif col_needed[j] == 'model':
                    model = dictionary[col_needed[j]].title()
                    new_line.append(model)
                elif col_needed[j] == 'brand':
                    brand = dictionary[col_needed[j]].title()
                    new_line.append(brand)
                else:
                    new_line.append(dictionary[col_needed[j]])
            new_query = make_query(_col, new_line)
            # print new_query
            try:
                cursor.execute(new_query)
                db.commit()
            except:
                pass

            if i == 10000:
                break
        i += 1


# disconnect from server
db.close()