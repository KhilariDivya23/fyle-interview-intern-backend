from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))

    @classmethod
    def bad_request(cls, data, error="", message=""):
        return make_response(jsonify(error=error, message=message), 400)

    @classmethod
    def not_found(cls, data, error="", message=""):
        return make_response(jsonify(error=error, message=message), 404)
