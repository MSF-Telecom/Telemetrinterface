const userDB = require('../usersDB.json')

teleData = {temp: 21.5, hum: 42, press: 1023, 
            in1: false, in2: false, in3: false, in4: false,
            out1: false, out2: false, out3: false, out4: false,
            ain1: 1352, ain2: 532, ain3: 84, ain4: 3045}

exports.controlPage = function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      res.render('control/main.ejs', {data: teleData})
    }
    else {
      res.redirect('/login')
    }
  }
  else{
    res.redirect('/login')
  }
}

exports.OIOut = function (req, res) {
  let outputs = [req.body.OUT1, req.body.OUT2, req.body.OUT3, req.body.OUT4]
  console.log(outputs)
  teleData.out1 = outputs[0]
  teleData.out2 = outputs[1]
  teleData.out3 = outputs[2]
  teleData.out4 = outputs[3]

  res.redirect('/control')
}