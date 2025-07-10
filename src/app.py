"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/members", methods=["GET"])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/members/<int:id>", methods=["GET"])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/members", methods=["POST"])
def add_member():
    try:
        data = request.get_json()
        required_fields = ["first_name", "age", "lucky_numbers"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        jackson_family.add_member(data)#Que tenga que añadir la informacion de vuelta deveria de haberse avisado me ha costado un buen rato a solucionarlo
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        deleted = jackson_family.delete_member(id)
        if deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

""" @app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200 """



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
