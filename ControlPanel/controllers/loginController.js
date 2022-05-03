const secrets = require('../secrets.json')
const config = require('../config.json')
const crypto = require("crypto")

const fs = require('fs');

var loginMessage = ''

exports.loginGET = function (req, res) {
  if (config.status.login == 'live' || config.status.login == 'test') {
    res.render('login.ejs', {login_message: loginMessage})
  } else if (config.status.login == 'maintenance') {
    res.render('maintenance.ejs')
  }
}

exports.loginPOST = function (req, res) {
  if (config.status.login == 'live' || config.status.login == 'test') {
    const data = fs.readFileSync('usersDB.json', 'utf8')
    const userDB = JSON.parse(data)

    let username = req.body.username
    let password = req.body.password
    passwordSHA256 = crypto.createHash('sha256').update(password).digest('hex')
    if (userDB.hasOwnProperty(username)){
      let active = userDB[username].active
      if(!active) {
        loginMessage = 'Account not activated'
        res.redirect('/login')
      } else {
        if (passwordSHA256 == userDB[username].passwordSHA256) {
          //req.session.user = { name: username }
          req.session.user = { name: username, privileges: userDB[username].privileges }
          loginMessage = ''
          res.redirect('/user')
        } else {
          loginMessage = 'Incorrect password'
          res.redirect('/login')
        }
      }
    }
    else {
      loginMessage = 'Username not found'
      res.redirect('/login')
    }
  } else if (config.status.login == 'maintenance') {
    res.render('maintenance.ejs')
  }
}

exports.registerGET = function (req, res) {
  if (config.status.register == 'live' || config.status.register == 'test') {
    res.render('user/register/register.ejs')
  } else if (config.status.register == 'maintenance') {
    res.render('maintenance.ejs')
  }
}

exports.registerPOST = function (req, res) {
  if (config.status.register == 'live' || config.status.register == 'test') {
    const data = fs.readFileSync('usersDB.json', 'utf8')
    const userDB = JSON.parse(data)

    let username = req.body.username
    let password = req.body.password
    let confirmPassword = req.body.confirmpassword

    let passwordSHA256 = crypto.createHash('sha256').update(password).digest('hex')
    if (userDB.hasOwnProperty(username)) {
      res.redirect('/login')
    } else if (password != confirmPassword) {
      res.redirect('/register')
    } else {
      userDB[username] = { passwordSHA256: passwordSHA256, active : false, privileges : 1 }
      const data = JSON.stringify(userDB, null, 4);
      fs.writeFile('usersDB.json', data, (err) => {
        if (err) {
          console.log(`Error writing file: ${err}`)
        }})
      res.render('user/register/registerDone.ejs')
    }
  } else if (config.status.register == 'maintenance') {
    res.render('maintenance.ejs')
  }
}

exports.logout = function (req, res) {
  if (config.status.logout == 'live' || config.status.logout == 'test') {
    req.session.destroy()
    res.redirect('/')
  } else if (config.status.logout == 'maintenance') {
    res.render('maintenance.ejs')
  }
}