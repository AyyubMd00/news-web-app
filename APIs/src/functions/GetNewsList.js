const { app } = require('@azure/functions');
const jwt = require('jsonwebtoken');
const NewsDao = require('../dao/newsDao');
const newsDao = new NewsDao();
const Responses = require('../utils/Responses');
const responses = new Responses();
const jwToken = require('../Config').get().jwt.token;

app.http('GetNewsList', {
    methods: ['GET'],
    authLeavel: 'anonymous',
    handler: async (request, context) => {
        const authorization = request.headers.get('authorization');
        if (!authorization) {
            return responses.sendBadRequestResponse('Missing Authorization Header!');
        }
        const token = authorization.split(" ")[1];
        let userId;
        try {
            const credentials = jwt.verify(token, jwToken);
            userId = credentials.user_id;
        }
        catch {
            return responses.sendAuthFailedResponse('Invalid Auth Token');
        }
        let category = request.query.get('category');
        let timestamp = request.query.get('timestamp');
        let news_list = await newsDao.getNewsList(category, timestamp);
        context.log('News Count:', news_list.length);
        let response = {
            message: "News is fetched",
            news_list: news_list
        }
        return responses.sendSuccessResponse(response);    
    }   
});

module.exports = app;