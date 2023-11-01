from routers.database.mongo_connection import MongoConnection
from routers.users.models.user_model import Images


class FormActions:
    def __init__(self, form_data):
        self.data = form_data

    @staticmethod
    def id_counter(request_type):
        with MongoConnection() as client:
            id = client.id.find_one({"type": request_type})
            if id:
                client.id.update_one({"type": request_type}, {"$inc": {"counter": 1}})
                return id.get("counter")
            else:
                client.id.insert_one({"type": request_type, "counter": 1})
                return 1

    def create_form(self):
        with MongoConnection() as client:
            self.data['referralNumber'] = self.id_counter("forms")
            self.data['confirmed'] = False
            client.forms.insert_one(self.data)
            return {"success": True, "message": "Form registered successfully",
                    "referralNumber": self.data['referralNumber']}

    @staticmethod
    def confirm_form(referral):
        with MongoConnection() as client:
            form = client.forms.update_one({"referralNumber": referral}, {"$set": {"confirmed": True}})
            if form.modified_count:
                return {"success": True, "message": "Form confirmed successfully"}
            return {"success": True, "message": "something went wrong!"}

    @staticmethod
    def get_forms(company_id):
        with MongoConnection() as client:
            return {"success": True, "message": list(client.forms.aggregate(
                [
                    {
                        '$match': {
                            'companyID': int(company_id)
                        }
                    }, {
                    '$project': {
                        '_id': 0
                    }
                }]))}

    @staticmethod
    def add_image_to_form(username, docs):
        images = Images()
        url = images.set_avatar_file(username, username, docs)
        with MongoConnection() as client:
            client.users.update_one({"username": username}, {"$set": {"avatar": url}})
            return {"message": "User registered successfully"}
