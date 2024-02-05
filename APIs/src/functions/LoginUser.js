const { app } = require('@azure/functions');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const jwToken = require('../Config').get().jwt.token;
const UsersDao = require('../dao/usersDao.js');
const usersDao = new UsersDao();
const Responses = require('../utils/Responses');
const responses = new Responses();
const saltRounds = 10;

app.http('LoginUser', {
    methods: ['POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        let requestBody = await request.json();
        context.log(requestBody);
        if (!requestBody) {
            return responses.sendBadRequestResponse('Request body is missing!');
        }
        context.log('Request body:', request);
        if (!requestBody.email) {
            return responses.sendBadRequestResponse('Email is missing!');
        }
        if (!requestBody.password) {
            return responses.sendBadRequestResponse('Password is missing!');
        }
        let user = await usersDao.getPassword(requestBody.email);
        if (!user || !await bcrypt.compare(requestBody.password, user.password)) {
            return responses.sendBadRequestResponse('Incorrect Email or Password!');
        }
        const token = jwt.sign(user, jwToken, {
            expiresIn: '24h'
        });
        let response = {
            message: 'Login successful',
            token: token
        };
        return responses.sendSuccessResponse(response);
    }
});