// connect to mysql db
var mysql = require('mysql');
var connection = mysql.createConnection({
  host     : 'project.c34htetfwwf4.us-east-1.rds.amazonaws.com',
  user     : 'wuzhengx',
  password : '11111111',
  database : 'cis550project'
});

var express = require('express');
var passport = require('passport');
var router = express.Router();

var Twitter = require('twitter');

var request = require('request');

// homepage
router.get('/', function(req, res) {
  res.render('homepage.ejs');
});

router.get('/create', function(req, res) {
  res.render('homepage.ejs');
});

router.get('/admin', function(req, res) {

  var query_1 = "SELECT COUNT(*) as c FROM (\
                SELECT COUNT(*) FROM cars C GROUP BY C.make\
                ) CC;";
  var query_2 = "SELECT COUNT(*) as c FROM cars C;";
  var query_3 = "SELECT COUNT(DISTINCT S.email) as c FROM subscriber S;";
  var query_4 = "SELECT COUNT(*) as c FROM used_cars_info C;";
  var query_5 = "SELECT * FROM comments Order By time DESC LIMIT 5;";

  connection.query(query_1, function(err, row_1, fields) {
    if (err) console.log(err);
    else {
            connection.query(query_2, function(err, row_2, fields) {
              if (err) console.log(err);
              else {

                      connection.query(query_3, function(err, row_3, fields) {
                        if (err) console.log(err);
                        else {

                                  connection.query(query_4, function(err, row_4, fields) {
                                    if (err) console.log(err);
                                    else {
                                            connection.query(query_5, function(err, row_5, fields) {
                                              if (err) console.log(err);
                                              else {
                                                        var parts = row_5[0].time.toString().split(" ");
                                                        //console.log(parts[0] + " " + parts[1] + " " + parts[2] + " " + parts[3]);
                                                        row_5[0].curr_time = parts[0] + " " + parts[1] + " " + parts[2] + " " + parts[3];

                                                        var parts_2 = row_5[1].time.toString().split(" ");
                                                        //console.log(parts[0] + " " + parts[1] + " " + parts[2] + " " + parts[3]);
                                                        row_5[1].curr_time = parts_2[0] + " " + parts_2[1] + " " + parts_2[2] + " " + parts_2[3];

                                                        res.render('admin.ejs', 
                                                        {
                                                          brand_count : row_1[0].c,
                                                          new_car_count : row_2[0].c,
                                                          used_car_count : row_4[0].c,
                                                          subscriber_count : row_3[0].c, 
                                                          comments_1 : row_5[0], 
                                                          comments_2 : row_5[1]
                                                        });
                                                  }
                                            });

                                        }
                                  }); 

                            }
                      }); 

                  }
            }); 
        }
  }); 
});


                                            

router.get('/subscribe', function(req, res) {
  // adding to the database
  var email_insert = "INSERT INTO subscriber (email) VALUES('" + req.query.Email + "');"
   connection.query(email_insert, function(err, row, fields) {
                    if (err) console.log(err);
                    else {
                            res.render('searchmainplain.ejs');
                        }
                  });   
});

/**
 * You first need to create a formatting function to pad numbers to two digits…
 **/
function twoDigits(d) {
    if(0 <= d && d < 10) return "0" + d.toString();
    if(-10 < d && d < 0) return "-0" + (-1*d).toString();
    return d.toString();
}

/**
 * …and then create the method to output the date string as desired.
 * Some people hate using prototypes this way, but if you are going
 * to apply this to more than one Date object, having it as a prototype
 * makes sense.
 **/
Date.prototype.toMysqlFormat = function() {
    return this.getUTCFullYear() + "-" + twoDigits(1 + this.getUTCMonth()) + "-" + twoDigits(this.getUTCDate()) + " " + twoDigits(this.getUTCHours()) + ":" + twoDigits(this.getUTCMinutes()) + ":" + twoDigits(this.getUTCSeconds());
};

router.get('/comment', function(req, res) {
  var myDate_string = new Date().toMysqlFormat();
  // adding to the database
  var comment_insert = "INSERT INTO comments (email, name, comments, time) \
                      VALUES('" + req.query.Email + "', '" + req.query.Name + "', \
                        '" + req.query.Message + "', '" + myDate_string +  "');";
   
   connection.query(comment_insert, function(err, row, fields) {
                    if (err) console.log(err);
                    else {
                            res.render('searchmainplain.ejs');
                        }
                  });   
});

router.post('/newlogin', function(req, res) {
  var succ = 0;
  if (req.body.login == 'login') {

    // access database to verify
    if (succ == 0) {
      console.log(req);
      if (req.body.user == 'admin') {
        // just for testing
        if (succ == 0) {
          res.redirect('/admin');
        } else {
          res.render('error.ejs');
        }
      } else {
        res.render('searchmainplain.ejs');
      }
    } else {
        // TODO: modified to be tokenized
        // way to auth. Redirect to a page
        res.render('searchmainplain.ejs');
      
    }
  } else {
    if (req.body.user == 'admin') {
        res.render('error.ejs');
      } else {
        // create account in database
        res.render('msg.ejs');
      }
  }
});


router.get('/err', function(req, res, next) {
  res.render('err.ejs');
});

router.get('/msg', function(req, res, next) {
  res.render('msg.ejs');
});

// modified logout function
router.get('/logout', function(req, res) {
  req.session.destroy(function (err) {
    res.redirect('/');
  });
});

router.post('/signup', passport.authenticate('local-signup', {
  successRedirect: '/msg',
  failureRedirect: '/err',
  failureFlash: true,
}));

router.post('/login', passport.authenticate('local-login', {
  successRedirect: '/searchmainplain',
  failureRedirect: '/err',
  failureFlash: true,
}));


// homepage
router.get('/homepage', function(req, res) {
  res.render('homepage.ejs');
});

router.get('/auth/facebook', passport.authenticate('facebook', { scope: 'email' }));

router.get('/auth/facebook/callback', passport.authenticate('facebook', {
  successRedirect: '/profile',
  failureRedirect: '/',
}));

router.get('/auth/twitter', passport.authenticate('twitter'));

router.get('/auth/twitter/callback', passport.authenticate('twitter', {
  successRedirect: '/twitterfeeds',
  failureRedirect: '/',
}));

// display twitter feeds of this user
router.get('/twitterfeeds', function(req, res) {

  var client = new Twitter({
  consumer_key: 'vZ1KblNI6Q29fDs6abo9Ozgy4',
  consumer_secret: 'cModj4jzV51P1ywQPi2yHdNqfBNm5VdVWJwceIv5rCytOWFoHF',
  access_token_key: req.user.token,
  access_token_secret: req.user.tokenSecret
  });
  //console.log(req.user)
  var params = {screen_name: req.user.twitter.displayName};

  var results = [];
  client.get('search/tweets', {q: 'usedcars'}, function(error, tweets, response) {
    if (!error) {
      console.log(tweets.statuses[0].user.screen_name)
      var i;
      for (i = 0; i < 5; i++) {
        results.push({ text : tweets.statuses[i].text, username: tweets.statuses[i].user.screen_name });
        //console.log(results)
      }
      //res.render('test.ejs');
      res.render('searchmain.ejs', 
            {feeds: results}
      );
    }
  });
});

// display out the search result page
router.get('/search', function(req, res) {

  // query on db

  // get back 

  // website search  
  var GoogleSearch = require('google-search');
  var googleSearch = new GoogleSearch({
    key: 'AIzaSyDx-9VsMyFgLcGW31ogMbz4J7V3q8TRKiI',
    cx: '015274493814089078993:ghgb7wu8nea'
  });
  
  var condition;
  if (req.query.used == 'false') {
    condition = 'new';
  } else {
    condition = 'used';
  }
  var _searchQuery = condition + ' ' + req.query.Make + ' ' + req.query.Model + ' ' + req.query.Year;
  var _imageQuery = req.query.Make + ' ' + req.query.Model;

  var searchResults = [];
  var imageResults = [];
  googleSearch.build({
    // dynamic query
    q: _searchQuery,
    start: 5,
    num: 10, // Number of search results to return between 1 and 10, inclusive 
  }, function(error, response) {
        for (var i = 0; i < 5; i++) {
            searchResults.push({ title: response.items[i].title, link: response.items[i].link, snippet: response.items[i].snippet });
        }
        // image search
      const GoogleImages = require('google-images');
      const client = new GoogleImages('15274493814089078993:ghgb7wu8nea', 'AIzaSyDx-9VsMyFgLcGW31ogMbz4J7V3q8TRKiI');
     // dynamic query
      client.search(_imageQuery)
        .then(images => {
             //console.log(searchResults);
             for (var i = 0; i < 5; i++) {
                imageResults.push( { url: images[i].url} );
             }
             //console.log(imageResults);
             // rendering the page with those two sources
             console.log(req.query)

             query = "SELECT DISTINCT C.make, UC.postal_code, UC.year_of_registration, UC.price, UC.vehicle_model\
                      FROM cars C INNER JOIN used_cars_info UC\
                                  ON C.make = UC.vehicle_brand\
                                  INNER JOIN engine E_OUT\
                                  ON C.engine_code = E_OUT.engine_code\
                            WHERE E_OUT.engine_hp > (\
                              SELECT avg(E_IN.engine_hp)\
                              FROM cars C_IN INNER JOIN engine E_IN\
                              ON C_IN.engine_code = E_IN.engine_code\
                              WHERE C_IN.make = " + "'" + req.query.Make + "'" +"\
                              ) AND C.make = " + "'" + req.query.Make + "'" + " AND UC.year_of_registration >= " + req.query.Year + "\
                            AND UC.vehicle_model = " + "'" + req.query.Model + "'" + "\
                            AND UC.price > 10000\
                            ORDER BY UC.price DESC\
                            LIMIT 10;";
  
            connection.query(query, function(err, rows, fields) {
              if (err) console.log(err);
              else {
                console.log(rows)

                // call those queries getting other detailed info about the car
                car_detail_query = "SELECT DISTINCT E_OUT.engine_hp, E_OUT.engine_fuel_type, \
                                  AVG(C.highway_mpg) as highway_mpg, AVG(C.city_mpg) as city_mpg, AVG(C.msrp) as msrp, AVG(UC.price) + 10000 as used_price\
                                  FROM cars C INNER JOIN engine E_OUT\
                                              ON C.engine_code = E_OUT.engine_code\
                                              INNER JOIN used_cars_info UC\
                                              ON C.make = UC.vehicle_brand\
                                  WHERE C.make = " + "'" + req.query.Make + "'" + "AND \
                                  C.model = " + "'" + req.query.Model + "';" 

                 connection.query(car_detail_query, function(err, car_detail_row, fields) {
                if (err) console.log(err);
                else {
                      console.log(car_detail_row[0]);
                      var str = car_detail_row[0].engine_fuel_type.toString();
                      var parts = str.split(" ");
                      car_detail_row.engine_fuel = parts[0];
                      car_detail_row.used_msrp = Math.floor( car_detail_row[0].used_price );
                      console.log(car_detail_row)



                      // running recommendations query
                      recommendation_query = "SELECT DISTINCT C.make, C.model\
                                              FROM cars C\
                                              WHERE msrp > (\
                                                SELECT AVG(C_IN.msrp)\
                                                  FROM cars C_IN\
                                                ) AND exists (\
                                                  SELECT *\
                                                  FROM used_cars_info UC\
                                                  WHERE C.make = UC.vehicle_brand \
                                                      AND UC.year_of_registration > 2008\
                                                ) AND C.make = " + "'" +  req.query.Make  + "'" + "\
                                                AND C.popularity > (\
                                                    SELECT AVG(C_IN_IN.popularity)\
                                                    FROM cars C_IN_IN\
                                                  ) \
                                                ORDER BY C.popularity\
                                                LIMIT 5;"

                       connection.query(recommendation_query, function(err, recommendation_row, fields) {
                          if (err) console.log(err);
                          else {
                                console.log(recommendation_row)
                                                res.render('searchresults.ejs', { query_result: rows,
                                                  car_detail_result: car_detail_row,
                                                  recommendation_result: recommendation_row,
                                                  query: req.query,
                                                  searchResults: searchResults, 
                                                  imageResults: imageResults
                                                });                               



                              }
                        });                          


                      }
                });
              }
            });
        });
  });
});

router.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));

// router.get('/auth/google/callback', passport.authenticate('google', {
//   successRedirect: '/plain',
//   failureRedirect: '/plain',
// }));

router.get('/auth/google/callback', function(req, res) {
  res.render('searchmainplain.ejs');
});

router.get('/searchmainplain', function(req, res) {
  res.render('searchmainplain.ejs');
});

module.exports = router;

function isLoggedIn(req, res, next) {
  if (req.isAuthenticated())
      return next();
  res.redirect('/');
}
