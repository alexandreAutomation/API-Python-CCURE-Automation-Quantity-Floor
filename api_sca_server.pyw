from flask import request as reque, Flask, make_response
from flask_restful import Resource, Api
from json import load

app = Flask(__name__)
api = Api(app)


def api_cw():
    return load(open('floor.json', 'r', encoding= 'utf-8'))


class Greet(Resource):

    def __init__(self):
        self.req = reque.get_json()
        self.resp = api_cw()

    def get(self):
        return self.resp

    def post(self):
        return self.req, 200, {'Accept': 'application/json'}


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers)
    return resp


api.add_resource(Greet, '/sca')
config_json = open('dist/config_network', 'r').readline().split(';')
if __name__ == "__main__":
    app.run(port=config_json[1], host=str(config_json[0]))
