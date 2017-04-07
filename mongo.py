#####################################
# 1. Install pymongo
# 2. Start an instance
# 3. Python connect to mongodb://wuzhengx:Aa1111111@ds155150.mlab.com:55150/car_brand
# 4. Create tables and populate

# Arthur:
# Zhengxuan Wu, Fengkai Wu, Mengyi Cui
# University Of Pennsylvania
#####################################
from pymongo import MongoClient


client = MongoClient()
client = MongoClient("mongodb://wuzhengx:Aa1111111@ds155150.mlab.com:55150/car_brand")
db = client['car_brand']
posts = db.posts
#db.car_brand.insert_one({"car_brand" : "test_wuzhengx", "html" : "this is shit!!!!!"});
import os
rootdir ='/Users/Frank/Desktop/CIS550F/CIS550Project/xml_data'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
    	 f = open(rootdir + '/' + file,'r')
    	 #print f.name
    	 if f.name.split('.')[1] == "html":
    	 	print f.name
            	new_file=f.read()
            	#print new_file
            	print "inserting " + f.name.split('.')[0].split('/')[-1]
            	db.car_brand.insert_one({"car_brand" : f.name.split('.')[0].split('/')[-1], "html" : new_file});

print "Success!!"
