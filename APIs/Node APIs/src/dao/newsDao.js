const MongoHandler = require('../MongoHandler.js');
const mongoHandler = new MongoHandler();

class NewsDao {
    // connecting to 'english_news' collection in mongo DB
    async init() {
        this.collection = await mongoHandler.connectToCollection('english_news');
    }

    async getNewsList(category, timestamp) {
        await this.init();
        const pageSize = 20;
        const query = {};
        if (timestamp) {
            query.published_timestamp = {'$lt': timestamp};
        }
        if (category) {
            query.category = category;
        }
        const project = {
            _id: 0,
            article_id: 1,
            title: 1,
            source_id: 1,
            image_url: 1,
            published_timestamp: 1,
            category: 1
        };
        const sort = {
            published_timestamp: -1
        };
        const documents = await this.collection.find(query).project(project).sort(sort).limit(pageSize).toArray();
        await mongoHandler.closeConnection();
        return documents;
    };

    async getNewsDetail(article_id) {
        await this.init();
        const query = {article_id: article_id};
        const options = {
            projection: {
                _id: 0,
                article_id: 1,
                title: 1,
                source_id: 1,
                image_url: 1,
                published_timestamp: 1,
                category: 1,
                link: 1,
                language: 1,
                video_url: 1,
                tags: 1,
                description: 1,
                updated_timestamp: 1,
                city_name: 1,
                country: 1,
                author: 1,
                content: 1
            }
        };
        const document = await this.collection.findOne(query, options);
        await mongoHandler.closeConnection();
        return document;
    }
};

module.exports = NewsDao;