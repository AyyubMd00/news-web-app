const { app } = require('@azure/functions');
const bcrypt = require('bcryptjs');
const { v4: uuid4 } = require('uuid');
const validator = require('../utils/Validator');
const UsersDao = require('../dao/usersDao.js');
const usersDao = new UsersDao();
const Responses = require('../utils/Responses');
const responses = new Responses();
const saltRounds = 10;

app.http('RegisterUser', {
    methods: ['POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        let requestBody = {}
        try {
            requestBody = await request.json();
            context.log(requestBody)
        }
        catch {
            return responses.sendBadRequestResponse('Request body is missing!');
        }
        if (!requestBody.email) {
            return responses.sendBadRequestResponse('Email is missing!');
        }
        if (!requestBody.password) {
            return responses.sendBadRequestResponse('Password is missing!');
        }
        if (!requestBody.name) {
            return responses.sendBadRequestResponse('Name is missing!');
        }
        if (typeof requestBody.name !== 'string') {
            return responses.sendBadRequestResponse('Name should be a string!');
        }
        if (!validator.validateName(requestBody.name)) {
            return responses.sendBadRequestResponse('Name should not contain any special characters!');
        }
        if (!requestBody.age) {
            return responses.sendBadRequestResponse('Age is missing!');
        }
        if (!validator.validateEmail(requestBody.email)) {
            return responses.sendBadRequestResponse('Invalid email!');
        }
        if (!validator.validatePassword(requestBody.password)) {
            return responses.sendBadRequestResponse('Password should be of atleast 8 characters and should contain atleast one upper case letter, one lower case letter, one number and one special character!');
        }
        if (requestBody.age < 10) {
            return responses.sendBadRequestResponse('Age must be greater than or equal to 10!');
        }
    
        let passwordHash = await bcrypt.hash(requestBody.password, saltRounds);
        context.log(passwordHash);
        
        if (await usersDao.checkExistingUser(requestBody.email)) {
            return responses.sendBadRequestResponse(`User with email ${requestBody.email} exists already!`)
        }

        const currentTime = new Date();
        const currentTimeInISO = currentTime.toISOString();

        const newUser = {
            user_id: uuid4(),
            name: requestBody.name,
            email: requestBody.email,
            password: passwordHash,
            age: requestBody.age,
            created_timestamp: currentTimeInISO
        }

        if (!await usersDao.addUser(newUser)) {
            return responses.sendInternalServerErrorResponse('Failed to add user!')
        }
        
        let response = {
            message: "User added"
        };
        return responses.sendSuccessResponse(response);
    }
});