const secrets = require('../secrets.json')
const config = require('../config.json')

exports.homePage = function (req, res) {
  if (config.status.homepage == 'live' || config.status.homepage == 'test') {
    res.render('homepage.ejs', {user: req.session.user})
  } else if (config.status.homepage == 'maintenance') {
    res.render('maintenance.ejs')
  }
}

exports.about = function (req, res) {
  if (config.status.about == 'live' || config.status.about == 'test') {
    res.render('about.ejs')
  }
  else if (config.status.about == 'maintenance') {
    res.render('maintenance.ejs')
  }
}