const axios = require('axios')

exports.outputs = async function (nodeID, outputs) {
  await axios.post('http://127.0.0.1:8081/control/outputs', {
      nodeID: nodeID,
      outputs: outputs
  })
}

exports.buzzer = async function (nodeID, buzzTime) {
  await axios.post('http://127.0.0.1:8081/control/buzzer', {
      nodeID: nodeID,
      buzzTime: buzzTime
  })
}

exports.leds = async function (nodeID, RGB) {
  await axios.post('http://127.0.0.1:8081/control/leds', {
    nodeID: nodeID,
    RGB: RGB
  })
}