import redis
import json
from uuid import uuid4

class redisDao:
    r = redis.Redis(
        host='composed-mongoose-54491.upstash.io',
        port=6379,
        password='AdTbAAIncDEwN2Q1NWEwYWM2NzA0ZTdhYWNiOWM0ZTY1OTNhNmUyZXAxNTQ0OTE',
        ssl=True
    )

    def load_data(self, json_obj, key):
        obj_id = str(uuid4())
        self.r.sadd(key, obj_id)
        self.r.set(obj_id, json.dumps(json_obj))

    def get_user_hist(self, user_id):
        hist_ids_list = self.r.smembers(user_id)
        hist_list = []
        for id in hist_ids_list:
            hist_list.append(json.loads(self.r.get(id)))
        return hist_list

    def get_user_tags(self, user_id):
        return json.loads(self.r.get(user_id))