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

router.post('/newlogin', function(req, res) {
  var succ = 0;
  if (req.body.login == 'login') {

    // access database to verify
    if (succ == 0) {
      console.log(req);
      if (req.body.user == 'admin') {
        // just for testing
        if (succ == 0) {
          res.render('admin.ejs');
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
                              ) AND C.make = " + "'" + req.query.Make + "'" + " AND UC.year_of_registration > " + req.query.Year + "\
                            AND UC.vehicle_model = " + "'" + req.query.Model + "'" + "\
                            AND UC.price > 10000\
                            ORDER BY UC.price DESC\
                            LIMIT 10;";
  
            connection.query(query, function(err, rows, fields) {
              if (err) console.log(err);
              else {
                console.log(rows)
                res.render('searchresults.ejs', { query_result: rows,
                                                  query: req.query,
                                                  searchResults: searchResults, 
                                                  imageResults: imageResults
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
