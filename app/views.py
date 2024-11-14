import sys

from flask.views import MethodView
from flask import jsonify, request
from models import AdModel, Session, ValidatatorAdModel


# test endpoint
def hello_world():
    return jsonify({"message": "hello world"})


class AdView(MethodView):
    def get(self, id_ad: int):
        try:
            with Session() as session:
                ad = session.query(AdModel).filter(AdModel.id == id_ad).first()
                return jsonify(
                    {
                        "id": ad.id,
                        "title": ad.title,
                        "created_at": ad.created_at,
                        "description": ad.description,
                        "owner": ad.owner,
                    }
                )
        except Exception as er:
            print(er, file=sys.stderr)
            raise AdViewError(400, "getting error")

    def post(self):
        json_data = dict(request.json)
        try:
            json_data_validate = ValidatatorAdModel(**json_data).dict()
        except Exception as er:
            print(er, file=sys.stderr)
            raise AdViewError(400, "validating error")
        try:
            with Session() as session:
                ads = AdModel(**json_data_validate)
                session.add(ads)
                session.commit()
                return jsonify(
                    {
                        "id": ads.id,
                        "title": ads.title,
                        "owner": ads.owner,
                        "description": ads.description,
                    }
                )
        except Exception as er:
            print(er, file=sys.stderr)
            raise AdViewError(400, "creating error")

    def delete(self, id_ad: str):
        try:
            with Session() as session:
                ad = session.query(AdModel).filter(AdModel.id == id_ad).first()
                session.delete(ad)
                session.commit()
                return jsonify({"status": "success"})
        except Exception as er:
            print(er, file=sys.stderr)
            raise AdViewError(400, "deleting error")


class AdViewError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def handle_invalid_adview_usage(error):
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response


def handle_invalid_usage(exception):
    print(exception, file=sys.stderr)
    response = jsonify({"message": "bad request"})
    response.status_code = 404
    return response
