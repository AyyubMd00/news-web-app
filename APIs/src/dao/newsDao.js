const connectToCollection = require('../MongoClient').connectToCollection;

class NewsDao {
    // connecting to 'english_news' collection in mongo DB
    async init() {
        this.collection = await connectToCollection('english_news');
    }

    async getNewsList(timestamp) {
        await this.init();
        const pageSize = 20;
        const query = {};
        if (timestamp) {
            query.created_timestamp = {'$lt': timestamp};
        }
        const documents = await this.collection.find(query).limit(pageSize).toArray();
        return documents;
    };
};

module.exports = NewsDao;