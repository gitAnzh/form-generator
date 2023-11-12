from routers.database.mongo_connection import MongoConnection
from routers.public_models.counter import id_counter


class FormActions:
    def __init__(self, form_data):
        self.data = form_data

    def create_form(self):
        with MongoConnection() as client:
            self.data['referralNumber'] = id_counter("forms")
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
    def get_forms(company_id, page, per_page):
        with MongoConnection() as client:
            page = page
            per = per_page
            skip = per * (page - 1)
            limit = per
            match = {'companyID': int(company_id)} if company_id is not None else {}

            data = list(client.forms.aggregate(
                [
                    {
                        '$match': match}, {
                    '$project': {
                        '_id': 0
                    }
                },
                    {"$skip": skip},
                    {"$limit": limit}
                ]))
            count = client.forms.count_documents(match)
            return {"success": True, "message": data, "count": count}

    @staticmethod
    def add_image_to_form(referral_number, docs):
        with MongoConnection() as client:
            client.forms.update_one({"referralNumber": int(referral_number)}, {"$set": {"docs": docs}})
            return {
                "message": f"Images successfully added to form, your referral number is {referral_number}, wait for our call, thanks"}

