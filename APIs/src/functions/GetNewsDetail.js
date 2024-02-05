const { app } = require('@azure/functions');
const jwt = require('jsonwebtoken');
const NewsDao = require('../dao/newsDao');
const newsDao = new NewsDao();
const Responses = require('../utils/Responses');
const responses = new Responses();
const jwToken = require('../Config').get().jwt.token;

app.http('GetNewsDetail', {
    methods: ['GET'],
    authLevel: 'anonymous',
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
        
        let article_id = request.query.get('article_id');
        if (!article_id) {
            return responses.sendBadRequestResponse('No article id is given!');
        }
        let article = await newsDao.getNewsDetail(article_id);
        if (!article) {
            return responses.sendBadRequestResponse('Incorrect article id is given!');
        }
        let response = {
            message: 'News article is fetched',
            article: article
        }
        return responses.sendSuccessResponse(response);
    }
});