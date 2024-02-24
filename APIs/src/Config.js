const config = {
    mongoDB: {
        connectionString: process.env.MongoDBConnString,
        database: "news_app"
    },
    jwt: {
        token: process.env.JsonWebToken
    }
};

console.log(config)

exports.get = function() {
    return config;
};