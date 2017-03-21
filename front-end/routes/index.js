var express = require('express');
var passport = require('passport');
var router = express.Router();

var Twitter = require('twitter');

router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/login', function(req, res, next) {
  res.render('login.ejs', { message: req.flash('loginMessage') });
});

router.get('/signup', function(req, res) {
  res.render('signup.ejs', { message: req.flash('signupMessage') });
});

router.get('/profile', isLoggedIn, function(req, res) {
  res.render('profile.ejs', { user: req.user });
});

// modified logout function
router.get('/logout', function(req, res) {
  req.session.destroy(function (err) {
    res.redirect('/');
  });
});

router.post('/signup', passport.authenticate('local-signup', {
  successRedirect: '/profile',
  failureRedirect: '/signup',
  failureFlash: true,
}));

router.post('/login', passport.authenticate('local-login', {
  successRedirect: '/profile',
  failureRedirect: '/login',
  failureFlash: true,
}));

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
  
  // website search  
  var GoogleSearch = require('google-search');
  var googleSearch = new GoogleSearch({
    key: 'AIzaSyDx-9VsMyFgLcGW31ogMbz4J7V3q8TRKiI',
    cx: '015274493814089078993:ghgb7wu8nea'
  });
   
  googleSearch.build({
    q: "used audi a5",
    start: 5,
    num: 10, // Number of search results to return between 1 and 10, inclusive 
  }, function(error, response) {
    console.log(response);
  });

  // image search
  const GoogleImages = require('google-images');
  const client = new GoogleImages('15274493814089078993:ghgb7wu8nea', 'AIzaSyDx-9VsMyFgLcGW31ogMbz4J7V3q8TRKiI');
 
  client.search('audi a5')
    .then(images => {
         console.log(images)
    });

  //res.render('searchresults.ejs');

});


router.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));

router.get('/auth/google/callback', passport.authenticate('google', {
  successRedirect: '/profile',
  failureRedirect: '/',
}));

module.exports = router;

function isLoggedIn(req, res, next) {
  if (req.isAuthenticated())
      return next();
  res.redirect('/');
}
