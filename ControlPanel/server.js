const express = require('express')
const cookieParser = require("cookie-parser")
const sessions = require('express-session')

const secrets = require('./secrets.json')
const routes = require('./routes')

const app = express()

const port = 8080

const oneDay = 1000 * 60 * 60 * 24

app.use(express.static('public'))
app.use(express.json({ limit: '5mb' }))

app.use(sessions({
  secret: secrets.sessionKey,
  saveUninitialized:true,
  cookie: { maxAge: oneDay },
  resave: false
}))

app.use(cookieParser())

app.use('/', routes)

app.listen(port, () => console.log(`Listening on port ${port}!`))