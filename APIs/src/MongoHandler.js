const { MongoClient } = require('mongodb');
const mongoConfig = require('./Config').get().mongoDB;

class MongoHandler {
    constructor() {
        this.client = new MongoClient(mongoConfig.connectionString);
    };
    async connectToCollection(collectionName) {
        try {
            await this.client.connect();
            const database = this.client.db(mongoConfig.database);
            const collection = database.collection(collectionName);
            return collection;
        }
        catch(error) {
            console.error('Mongo DB connection failed!', error);
            throw error;
        }
    };
    async closeConnection() {
        this.client.close();
    }
}

module.exports = MongoHandler;
