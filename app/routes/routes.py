from flask import Blueprint, jsonify, request, abort, make_response
from app.models.planet import Planet
from app import db

planets_bp = Blueprint('planets', __name__, url_prefix='/planets')

@planets_bp.route('', methods=['POST'])
def create_one_planet():
    if not request.is_json:
        return {'msg' : 'Missing json request body'}, 400
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

    rsp = {'msg' : f'Succesfully created planet with id {new_planet.id}'}
    return jsonify(rsp), 201


@planets_bp.route('', methods=['GET'])
def get_all_planets():
    params = request.args
    if 'color' in params and 'description' in params and 'name' in params:
        color = params['color']
        description = params['description']
        name = params['name']
        planets = Planet.query.filter_by(color=color, description=description, name=name)
    elif 'color'in params:
        color = params['color']
        planets = Planet.query.filter_by(color=color)
    elif 'description' in params:
        description = params['description']
        planets = Planet.query.filter_by(description=description)
    elif 'name' in params:
        name = params['name']
        planets = Planet.query.filter_by(name=name)
    else:
        planets = Planet.query.all()

    planets_response = []
    for planet in planets:
        planets_response.append(planet.get_dict())
    
    return jsonify(planets_response), 200


@planets_bp.route('/<planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return jsonify(planet.get_dict()), 200


@planets_bp.route('/<planet_id>', methods=['PUT'])
def update_one_planet(planet_id):
    planet = validate_planet(planet_id)

    if not request.is_json:
        return {'msg' : 'Missing json request body'}, 400

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

    rsp = {"msg" : f"Planet #{planet_id} successfully updated!"}
    return jsonify(rsp), 200


@planets_bp.route('/<planet_id>', methods=['DELETE'])
def delete_one_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    rsp = {'msg' : f'Planet #{planet.id} successfully deleted!'}
    return jsonify(rsp), 200


def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        rsp = {"msg" : f"Planet with id {planet_id} is invalid."}
        abort(make_response(rsp, 400))

    planet = Planet.query.get(planet_id)

    if not planet:
        rsp = {'msg' : f'Could not find planet with id {planet_id}.'}
        abort(make_response(rsp, 404))
    
    return planet
