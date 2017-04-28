## U.S. Used Car/New Car Database Project

Zhengxuan Wu, Mengyi Cui, Fengkai Wu
University Of Pennsylvania

## Architecture
* this is a website hold a new/used car infomation database. 
* it helps the user to query and retrieve useful infomation.

### Node.js Based Server
* the http server is built using node.js modules
* we have multiple active pages that exceeds the project requirements
* it contains: admin page; login page; search page; search result page
* it calls different APIs to make it even more useful: Google, Twitter, etc..
* this website contains cookied sessions to locate customers
### .ejs Based Front-end
* the front-end is built using .ejs frameworks, it is mainly in html format
* the front-end is also powered by W3, Google.
### Database System
* it involves: MongoDB, MySQL
* raw data types involves: .xml, .csv, .txt, etc..
* MongoDB contains 1 document type: brand_name (string), xml_file (string)
* MySQL contains multiple tables: cars, used_cars, cars_extra, user_info, login_info, subscriber, comment, etc..

## Prerequisites 
* [Git](http://git-scm.com/)
* [Node.js with npm](https://nodejs.org/en/)
* [MongoDB](https://docs.mongodb.org/manual/installation/)

## Installation (localhost; you need to config to use AWS EC2)

* ` git clone https://github.com/mengyicui/CIS550Project.git`
* `cd front-end`
* `npm install`
* `npm install twitter`
* `npm install mysql`
* `npm install google-search`
* `npm install --save google-images`
* You will need a Mongo instance running. In a new terminal window run `mongod` (EC2) -> `sudo service mongod start`
* `node app`

Head over to [http://localhost:3000](http://localhost:3000)
