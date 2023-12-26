const { app } = require('@azure/functions');
const NewsDao = require('../dao/newsDao');
const newsDao = new NewsDao();

app.http('GetNewsList', {
    methods: ['GET'],
    authLeavel: 'anonymous',
    handler: async (request, context) => {
        context.log(`Http function processed request for url "${request.url}"`);
        let documents = await newsDao.getNewsList();
        context.log('News Count:', documents.length);
        context.res = {
            status: 200, 
            body: {
                message: 'News is fetched',
                news_list: documents
            },
            headers: {
                'Content-Type': 'application/json'
            }
        };
        context.log(context.res);

        return context.res;
    }   
});

module.exports = app;