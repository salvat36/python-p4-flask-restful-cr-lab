#!/usr/bin/env python3

from flask import     (
    Flask,
    request,
    g,
    session,
    make_response,
    abort,
)

from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name", type=str)
parser.add_argument("image", type=str)
parser.add_argument("price", type=float)

class Plants(Resource):
    def get(self):

        response_dict = [p.to_dict() for p in Plant.query.all()]

        return make_response(
            response_dict, 
            200
        )
    
    def post(self):
        data = parser.parse_args()

        try:
            plant = Plant(**data)
            db.session.add(plant)
            db.session.commit()
        
        except:
            db.session.rollback()
            abort(400, "Houston we have a problem with the data")



api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        if plant := Plant.query.get(id):
            return make_response(plant.to_dict(), 200)
        else:
            abort(404, f"You need one of them stinking {id}")
        
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
