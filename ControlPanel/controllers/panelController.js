const userDB = require('../usersDB.json')
const dPyMRController = require('../controllers/dPyMRController')
const axios = require('axios')


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

exports.pollMode = function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      let nodeID = req.body.nodeID
      let mode = req.body.mode

      dPyMRController.mode(nodeID, mode)
      teleData[nodeID].mode = mode
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

exports.OIOut = function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      let nodeID = req.body.nodeID
      let outputs = [req.body.out1, req.body.out2, req.body.out3, req.body.out4]
      teleData[nodeID].out1 = outputs[0]
      teleData[nodeID].out2 = outputs[1]
      teleData[nodeID].out3 = outputs[2]
      teleData[nodeID].out4 = outputs[3]

      dPyMRController.outputs(nodeID, outputs)

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

      dPyMRController.buzzer(nodeID, buzzTime)
      
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

exports.IOLed = async function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      let nodeID = req.body.nodeID
      let RGB = req.body.RGB

      teleData[nodeID]['led1'] = [RGB[0], RGB[1], RGB[2]]
      teleData[nodeID]['led2'] = [RGB[3], RGB[4], RGB[5]]
      teleData[nodeID]['led3'] = [RGB[6], RGB[7], RGB[8]]
      teleData[nodeID]['led4'] = [RGB[9], RGB[10], RGB[11]]
      teleData[nodeID]['led5'] = [RGB[12], RGB[13], RGB[14]]

      dPyMRController.leds(nodeID, RGB)
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

exports.dataIn = function (req, res) {
  let data = req.body
  teleData = data
  res.send(teleData)
}

exports.askData = async function (req, res) {
  if(typeof req.session.user !== 'undefined') {
    if(userDB.hasOwnProperty(req.session.user.name) && userDB[req.session.user.name].active) {
      teleData = {}
      await axios.post('http://127.0.0.1:8081/control/nodes', {})
      .then((res) => {
        teleData = res.data
      })
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