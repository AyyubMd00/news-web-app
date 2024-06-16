from redis_data_producer import redisDao

RedisDao = redisDao()
def aggregate_tags(user_id):
    user_hist = RedisDao.get_user_hist(user_id)
    for item in user_hist:
        item['tags']