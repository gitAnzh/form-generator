import re

from routers.database.mongo_connection import mongo_client


def main_page_detail(search_by_companyName):
    with mongo_client() as client:
        match = {"status": True}
        if search_by_companyName:
            match = {"company_name": {
                '$regex': re.compile(rf"{search_by_companyName}(?i)")
            }}
        return list(client.users.aggregate([
            {
                '$match': match
            }, {
                '$project': {
                    'company_name': 1,
                    'avatar': 1,
                    '_id': 0
                }
            }
        ]))
