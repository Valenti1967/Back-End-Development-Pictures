from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture["id"] == id:
                return jsonify(picture), 200

        return {"message": "Picture not found"}, 404

    return {"message": "Internal server error"}, 500




######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json

    if not new_picture:
        return {"message":"Invalid input parameter"}, 422

    if data:
        for picture in data:
            if picture["id"] == new_picture["id"]:
                return {"Message": f"picture with id {picture['id']} already present"}, 302  

        data.append(new_picture)
        return jsonify(new_picture), 201
        
    return {"message": "Internal server error"}, 500
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):

    new_picture = request.json

    if not new_picture:
        return {"message":"Invalid input parameter"}, 422

    if data:

        for i in range(len(data)):
            if data[i]["id"] == id:
                data[i] = new_picture
                return jsonify(new_picture), 200

        return {"message": "Picture not found"}, 404

    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for picture in data:
            if picture["id"] == id:
                data.remove(picture)
                return "", 204

        return {"message": "Picture not found"}, 404

    return {"message": "Internal server error"}, 500
