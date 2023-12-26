const { MongoClient } = require('mongodb');
const mongoConfig = require('./Config').get().mongoDB;

exports.connectToCollection = async function(collectionName) {
    const client = new MongoClient(mongoConfig.connectionString);
    try {
        await client.connect();
        const database = client.db(mongoConfig.database);
        const collection = database.collection(collectionName);
        return collection;
    }
    catch {
        console.error('Mongo DB connection failed!', error);
        throw error;
    }
}
