from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, color):
        self.id = id
        self.name = name
        self.description = description
        self.color = color

    def get_dict(self):
        return  {
                'id' : self.id,
                'name' :  self.name,
                'description' : self.description,
                'color' :  self.color
            }
    
planets = [
    Planet(1, 'Mercury','Closest to the Sun and the smallest','slate gray'),
    Planet(2, 'Venus', 'Second planet from the Sun, little smaller than earth', 'yellow white'),
    Planet(3, 'Mars', 'Red planet has rocks and dusts', 'red')
]

planets_bp = Blueprint('planets', __name__, url_prefix='/planets')

@planets_bp.route('', methods=['GET'])
def get_all_planets():
    planets_response = []
    for planet in planets:
        planets_response.append(
            planet.get_dict()
        )

    return jsonify(planets_response)
    

@planets_bp.route('/<planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg" : f"Planet with id {planet_id} is invalid."}
        return jsonify(rsp), 400
        
    for planet in planets:
        if planet.id == planet_id:
            rsp = planet.get_dict()
    
            return jsonify(rsp), 200
    rsp = {
        "msg" : f"Could not find planet with id {planet_id}."
    }
    return jsonify(rsp), 404