from flask import Blueprint, jsonify, request
from app.models.planet import Planet
from app import db

# class Planet:
#     def __init__(self, id, name, description, color):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.color = color

#     def get_dict(self):
#         return  {
#                 'id' : self.id,
#                 'name' :  self.name,
#                 'description' : self.description,
#                 'color' :  self.color
#             }
    
# planets = [
#     Planet(1, 'Mercury','Closest to the Sun and the smallest','slate gray'),
#     Planet(2, 'Venus', 'Second planet from the Sun, little smaller than earth', 'yellow white'),
#     Planet(3, 'Mars', 'Red planet has rocks and dusts', 'red')
# ]

planets_bp = Blueprint('planets', __name__, url_prefix='/planets')

@planets_bp.route('', methods=['POST'])
def create_one_planet():
    request_body = request.get_json()
    try:
        name = request_body['name']
        description=request_body['description']
        color=request_body['color']
    except KeyError:
        return {'msg': 'failed to create new planet due to missing attributes'}, 400

    new_planet = Planet(name=name,
                        description=description,
                        color=color)
    db.session.add(new_planet)
    db.session.commit()

    return {
        'id' : new_planet.id,
        'msg' : f'Succesfully created planet with id {new_planet.id}'
    }, 201

@planets_bp.route('', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_response = []
    for planet in planets:
        planets_response.append({
            'id' : planet.id,
            'name' : planet.name,
            'description' : planet.description,
            'color' : planet.color
        })
    
    return jsonify(planets_response), 200





# @planets_bp.route('', methods=['GET'])
# def get_all_planets():
#     planets_response = []
#     for planet in planets:
#         planets_response.append(
#             planet.get_dict()
#         )

#     return jsonify(planets_response)
    

@planets_bp.route('/<planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg" : f"Planet with id {planet_id} is invalid."}
        return jsonify(rsp), 400
        
    planet = Planet.query.get(planet_id)
    if planet is None:
        rsp = {"msg" : f"Could not find planet with id {planet_id}."}
        return jsonify(rsp), 404

    rsp = {
        'id' : planet.id,
        'name' : planet.name,
        'color' :planet.color,
        'description' : planet.description
    }

    return jsonify(rsp), 200


@planets_bp.route('/<planet_id>', methods=['PUT'])
def update_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg" : f"Planet with id {planet_id} is invalid."}
        return jsonify(rsp), 400
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        rsp = {'msg' : f'Could not find planet with id {planet_id}.'}
        return jsonify(rsp), 404

    request_body = request.get_json()
    try:
        planet.name = request_body['name']
        planet.color = request_body['color']
        planet.description = request_body['description']
    except KeyError:
        return {
            'msg' : 'Update failed. name, color, and description are required!'
        }, 400

    db.session.commit()

    return {
        "msg" : f"Planet #{planet_id} successfully updated!"
    }, 200

@planets_bp.route('/<planet_id>', methods=['DELETE'])
def delete_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg" : f"Planet with id {planet_id} is invalid."}
        return jsonify(rsp), 400
    
    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        rsp = {'msg' : f'Could not find planet with id {planet_id}.'}
        return jsonify(rsp), 404

    db.session.delete(chosen_planet)
    db.session.commit()

    return {
        'msg' : f'Planet #{chosen_planet.id} successfully deleted!'
    }, 200




