const userDB = require('../usersDB.json')

teleData = {
      1107: {CPUTemp: [29.4, 36.5], CPUVolt: 1.1, Vers : 1.0, reset : 'none',
            push: true, pushTime: 10,
            temp: 21.5, hum: 42, press: 1023,
            accel : [9.81, 0.0, 0.0],
            in1: false, in2: false, in3: false, in4: false,
            out1: false, out2: false, out3: false, out4: false,
            ain1: 1352, ain2: 532, ain3: 84, vsup: 3045,
            led1 : [34,198,0], led2 : [12,0,230], led3 : [44,27,102],
            led4 : [0,44,128], led5 : [243,14,95]},
      1748: {CPUTemp: [23.4, 21.5], CPUVolt: 1.1, Vers : 1.0, reset : 'none',
            push: true, pushTime: 10,
            temp: 18, hum: 29, press: 998, 
            accel : [1.51, 3.8, 6.32],
            in1: false, in2: true, in3: false, in4: false,
            out1: false, out2: true, out3: false, out4: false,
            ain1: 204, ain2: 3997, ain3: 256, vsup: 5,
            led1 : [243,14,95], led2 : [34,198,0], led3 : [0,44,128],
            led4 : [12,0,230], led5 : [44,27,102]}
          }

exports.controlPage = function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      res.render('control/main.ejs', {data: teleData, nodeData: {}})
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
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      let nodeID = req.body.nodeID
      let outputs = [req.body.out1, req.body.out2, req.body.out3, req.body.out4]
      teleData[nodeID].out1 = outputs[0]
      teleData[nodeID].out2 = outputs[1]
      teleData[nodeID].out3 = outputs[2]
      teleData[nodeID].out4 = outputs[3]

      // #####################
      // #                   #
      // # Send data to node #
      // #                   #
      // #####################

      res.send(teleData)
    }
    else {
      res.redirect('/login')
    }
  }
  else{
    res.redirect('/login')
  }
}

exports.IOBuzzer = function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      let nodeID = req.body.nodeID
      let buzzTime = req.body.buzzTime

      // #####################
      // #                   #
      // # Send data to node #
      // #                   #
      // #####################
      
      console.log(nodeID + ', ' + buzzTime)
      res.send(teleData)
    }
    else {
      res.redirect('/login')
    }
  }
  else{
    res.redirect('/login')
  }
}

exports.IOLed = function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      let nodeID = req.body.nodeID
      let led = req.body.led
      let RGB = [req.body.R, req.body.G, req.body.B]
      teleData[nodeID]['led'+led] = RGB

      // #####################
      // #                   #
      // # Send data to node #
      // #                   #
      // #####################

      console.log(nodeID + ', ' + led + ', ' + RGB)
      res.send(teleData)
    }
    else {
      res.redirect('/login')
    }
  }
  else{
    res.redirect('/login')
  }
}

exports.dataOut = function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      res.send(teleData)
    }
    else {
      res.redirect('/login')
    }
  }
  else{
    res.redirect('/login')
  }
}