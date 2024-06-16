from redis_data_producer import redisDao
from aggregate_tags import aggregate_tags
from get_recommended_news import get_recommended_news

RedisDao = redisDao()

def process_hist(hist):
    user_id = hist['user_id']
    RedisDao.load_data(hist, user_id)
    aggregate_tags(user_id)
    get_recommended_news(user_id)