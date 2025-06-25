# server/app.py

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return "<h1>Pizza Restaurant API</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
     
    restaurants_data = [r.to_dict(rules=('-restaurant_pizzas',)) for r in restaurants]
    return make_response(jsonify(restaurants_data), 200)

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if not restaurant:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

    if request.method == 'GET':
        
        return make_response(jsonify(restaurant.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
     
        return make_response(jsonify({}), 204)

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
 
    pizzas_data = [p.to_dict(rules=('-restaurant_pizzas',)) for p in pizzas]
    return make_response(jsonify(pizzas_data), 200)

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
     
    try:
        new_rp = RestaurantPizza(
            price=data.get('price'),
            pizza_id=data.get('pizza_id'),
            restaurant_id=data.get('restaurant_id')
        )
        db.session.add(new_rp)
        db.session.commit()
         
        return make_response(jsonify(new_rp.to_dict()), 201)

    except Exception:
        # Catches the ValueError from our validation, or any other integrity error.
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)