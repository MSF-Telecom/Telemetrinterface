const express = require('express')
const bodyParser = require('body-parser')
const mainSiteController = require('./controllers/mainSiteController')
const userController = require('./controllers/userController')
const loginController = require('./controllers/loginController')
const router = express.Router()

router.use(bodyParser.urlencoded({ extended: true }))

router.get('/', mainSiteController.homePage)

router.get('/home', mainSiteController.homePage)

router.get('/about', mainSiteController.about)

router.get('/login', loginController.loginGET)

router.post('/login', loginController.loginPOST)

router.get('/register', loginController.registerGET)

router.post('/register', loginController.registerPOST)

router.get('/logout', loginController.logout)

router.get('/user', userController.userPage)

router.get('/user/psswd', userController.userNewPasswordGET)

router.post('/user/psswd', userController.userNewPasswordPOST)

router.get('/get',function(req, res){
  res.send(req.session)
})

router.all('*', function (req, res) {res.send('404')})

module.exports = router
