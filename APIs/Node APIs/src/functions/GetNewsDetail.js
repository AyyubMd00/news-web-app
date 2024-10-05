const { app } = require('@azure/functions');
const jwt = require('jsonwebtoken');
// const json = require('json');
const NewsDao = require('../dao/newsDao');
const newsDao = new NewsDao();
const Responses = require('../utils/Responses');
const responses = new Responses();
// const KafkaProducer = require('../utils/kafkaProducer');
// const kafkaProducer = new KafkaProducer();
const jwToken = require('../Config').get().jwt.token;
const axios = require('axios');

app.http('GetNewsDetail', {
    methods: ['GET'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        const authorization = request.headers.get('authorization');
        // if (!authorization) {
        //     return responses.sendBadRequestResponse('Missing Authorization Header!');
        // }
        let userId;
        if(authorization) {
            const token = authorization.split(" ")[1];
            try {
                const credentials = jwt.verify(token, jwToken);
                userId = credentials.user_id;
            }
            catch {
                return responses.sendAuthFailedResponse('Invalid Auth Token');
            }
        }
        
        let articleId = request.query.get('article_id');
        if (!articleId) {
            return responses.sendBadRequestResponse('No article id is given!');
        }
        let article = await newsDao.getNewsDetail(articleId);
        if (!article) {
            return responses.sendBadRequestResponse('Incorrect article id is given!');
        }
        if (article.tags == []) {
            article.tags == {}
        }
        // context.log(userId);
        if (authorization) {
            let userHistory = {
                user_id: userId,    
                article_id: articleId,
                tags: article.tags,
                timestamp: new Date().toISOString()
            };
            // kafkaProducer.publish(JSON.stringify(userHistory)); //not using await because API should not wait for the message to get produced.
            // Caling python API
            let kafkaAPIRes = await axios.post('https://func-news-app.azurewebsites.net/api/kafkaproducer', userHistory);
            if (kafkaAPIRes.status != 200) {
                await axios.post('https://func-news-app.azurewebsites.net/api/kafkaproducer', userHistory);
            }
            context.log(kafkaAPIRes.status);


        }
        let response = {
            message: 'News article is fetched',
            article: article
        }
        return responses.sendSuccessResponse(response);
    }
});