import os
from . import create_app
from .athlete import Athlete
from . import db
from flask import jsonify, request, abort

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/athlete/list", methods=["GET"])
def get_athletes():
    athletes = Athlete.query.all()
    return jsonify([athlete.to_json() for athlete in athletes])

@app.route("/athlete/<int:id>", methods=["GET"])
def get_athlete(id):
    athlete = Athlete.query.get(id)
    if athlete is None:
        abort(404)
    return jsonify(athlete.to_json())


@app.route("/athlete/<int:id>", methods=["DELETE"])
def delete_athlete(id):
    athlete = Athlete.query.get(id)
    if athlete is None:
        abort(404)
    db.session.delete(athlete)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/athlete', methods=['POST'])
def create_athlete():
    if not request.json:
        abort(400)
    athlete = Athlete(
        id=request.json.get('id'),
        firstname=request.json.get('firstname'),
        lastname=request.json.get('lastname'),
        city=request.json.get('city'),
        state=request.json.get('state'),
        country=request.json.get('country'),
        sex=request.json.get('sex')
    )
    db.session.add(athlete)
    db.session.commit()
    return jsonify(athlete.to_json()), 201

@app.route('/athlete/<int:id>', methods=['PUT'])
def update_athlete(id):
    if not request.json:
        abort(400)
    athlete = Athlete.query.get(id)
    if athlete is None:
        abort(404)
    athlete.id=request.json.get('id')
    athlete.firstname=request.json.get('firstname')
    athlete.lastname=request.json.get('lastname')
    athlete.city=request.json.get('city')
    athlete.state=request.json.get('state')
    athlete.country=request.json.get('country')
    athlete.sex=request.json.get('sex')
    db.session.commit()
    return jsonify(athlete.to_json())
