const secrets = require('../secrets.json')
const config = require('../config.json')
const crypto = require("crypto")

const fs = require('fs');

exports.userPage = function (req, res) {
  if (config.status.user == 'live' || config.status.user == 'test') {
    if(typeof req.session.user !== 'undefined') {
      res.render('user/user.ejs', { user_name : req.session.user.name })
    }
    else {
      res.redirect('/login')
    }
  } else if (config.status.user == 'maintenance') {
    res.render('maintenance.ejs')
  }
}

exports.userNewPasswordGET = function (req, res) {
  if (config.status.userNewPassword == 'live' || config.status.userNewPassword == 'test') {
    if(typeof req.session.user !== 'undefined') {
      res.render('user/password/NewPassword.ejs')
    }
    else {
      res.redirect('/login')
    }
  } else if (config.status.userNewPassword == 'maintenance') {
    res.render('maintenance.ejs')
  }
}

exports.userNewPasswordPOST = function (req, res) {
  if (config.status.userNewPassword == 'live' || config.status.userNewPassword == 'test') {
    const data = fs.readFileSync('usersDB.json', 'utf8')
    const userDB = JSON.parse(data)

    let username = req.session.user.name
    let password = req.body.password
    let confirmPassword = req.body.confirmpassword

    let newPasswordSHA256 = crypto.createHash('sha256').update(password).digest('hex')
    if (password != confirmPassword) {
      res.redirect('/user/newpassword')
    } else {
      userDB[username].passwordSHA256 = newPasswordSHA256
      const data = JSON.stringify(userDB, null, 4);
      fs.writeFile('usersDB.json', data, (err) => {
        if (err) {
          console.log(`Error writing file: ${err}`)
        }})
      res.render('user/password/NewPasswordDone.ejs')
    }
  } else if (config.status.userNewPassword == 'maintenance') {
    res.render('maintenance.ejs')
  }
}