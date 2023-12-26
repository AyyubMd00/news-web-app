const config = {
    mongoDB: {
        connectionString: "mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/",
        database: "news_app"
    }
};

exports.get = function() {
    return config;
};