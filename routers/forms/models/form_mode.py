from routers.database.mongo_connection import mongo_client


class FormActions:
    def __init__(self, referral_number):
        self.referral_number = referral_number

    def create_form(self, data: dict):
        with mongo_client() as client:
            data.update({"referralNumber": self.referral_number, "confirmed": False})
            client.forms.insert_one(data)
            return {"success": True, "referralNumber": self.referral_number}

    def confirm_form(self):
        with mongo_client() as client:
            form = client.forms.update_one({"referralNumber": self.referral_number}, {"$set": {"confirmed": True}})
            if form.modified_count:
                return {"success": True}
            return {"success": False}

    @staticmethod
    def get_forms(company_id, page, per_page):
        with mongo_client() as client:
            page = page
            per = per_page
            skip = per * (page - 1)
            limit = per
            match = {'companyID': int(company_id)} if company_id is not None else {}

            data = list(
                client.forms.aggregate(
                    [
                        {
                            '$match': match
                        },
                        {
                            '$project': {
                                '_id': 0,
                            }
                        },
                        {"$skip": skip},
                        {"$limit": limit}
                    ]
                )
            )
            count = client.forms.count_documents(match)
            return {"success": True, "count": count, "message": data}

    def add_image_to_form(self, doc_name):
        with mongo_client() as client:
            result = client.forms.update_one({"referralNumber": int(self.referral_number)}, {"$set": {"docs": doc_name}})
            if result.modified_count:
                return {"success": True}
            return {"success": False}
