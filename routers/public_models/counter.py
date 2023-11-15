from routers.database.mongo_connection import mongo_client


def id_counter(request_type):
    with mongo_client() as client:
        id_count = client.id.find_one({"type": request_type})
        if id_count:
            client.id.update_one({"type": request_type}, {"$inc": {"counter": 1}})
            return id_count.get("counter") + 1
        else:
            client.id.insert_one({"type": request_type, "counter": 1})
            return 1
