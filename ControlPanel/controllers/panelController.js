const userDB = require('../usersDB.json')

teleData = {
      1107: {temp: 21.5, hum: 42, press: 1023, 
            in1: false, in2: false, in3: false, in4: false,
            out1: false, out2: false, out3: false, out4: false,
            ain1: 1352, ain2: 532, ain3: 84, vsup: 3045},
      1748: {temp: 18, hum: 29, press: 998, 
        in1: false, in2: true, in3: false, in4: false,
        out1: false, out2: true, out3: false, out4: false,
        ain1: 204, ain2: 3997, ain3: 256, vsup: 5}
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