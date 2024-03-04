const MongoHandler = require('../MongoHandler.js');
const mongoHandler = new MongoHandler();

class UserDao {
    // connecting to 'user' collection in mongo DB
    async init() {
        this.collection = await mongoHandler.connectToCollection('users');
    }

    async addUser(user) {
        await this.init();
        const insertResult = await this.collection.insertOne(user);
        await mongoHandler.closeConnection();
        return insertResult.acknowledged;
    }

    async checkExistingUser(email) {
        await this.init();
        const query = {email: email};
        const options = {
            projection: {
                email: 1
            }
        };
        if (await this.collection.findOne(query, options) != null) {
            // await mongoHandler.closeConnection();
            return true;
        }
        // await mongoHandler.closeConnection();
        return false;
    }

    async getPassword(email) {
        await this.init();
        const query = {email: email};
        const options = {
            projection: {
                user_id: 1,
                email: 1,
                password: 1
            }
        };
        const user = await this.collection.findOne(query, options);
        await mongoHandler.closeConnection();
        return user;
    }
};

module.exports = UserDao;