exports.outputs = async function (nodeID, outputs) {
  await fetch('http://localhost:8081/control/outputs', {
    method: 'POST',
    body: JSON.stringify({
      nodeID: nodeID,
      outputs: outputs
    })
  })
}

exports.buzzer = async function (nodeID, buzzTime) {
  await fetch('http://127.0.0.1:8081/control/buzzer', {
    method: 'POST',
    body: JSON.stringify({
      nodeID: nodeID,
      buzzTime: buzzTime
    })
  })
}

exports.leds = async function (nodeID, led, RGB) {
  await fetch('http://127.0.0.1:8081/control/leds', {
    method: 'POST',
    body: JSON.stringify({
    nodeID: nodeID,
    leds: led,
    RGB: RGB
    })
  })
}