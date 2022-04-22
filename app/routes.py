from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, color):
        self.id = id
        self.name = name
        self.description = description
        self.color = color
    
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
            {
                'id' : planet.id,
                'name' : planet.name,
                'description' : planet.description,
                'color' : planet.color
            }
        )

    return jsonify(planets_response)
    