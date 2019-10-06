from flask import Flask, jsonify, request, abort
from datetime import datetime

from app import app, db
from app.models import measurement, user
from app import utils

@app.before_request
def check_auth_token():
    if request.path in ('/login', '/register', '/users', '/authenticate'):
        return

    if not request.headers.get('Authorization'):
        abort(401)


def authorize():
    token = request.headers.get('Authorization')
    return user.find_by_token(token)


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(user.get())


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    result = user.authenticate(
        username=body['username'],
        password=body['password']
    )
    if result:
        return jsonify(result)
    return "Wrong username or password", 400


@app.route('/authenticate', methods=['POST'])
def authenticate():
    body = request.get_json()
    result = user.find_by_token(token=body['token'])
    result['token'] = body['token']
    if result:
        return jsonify(result)
    return "Wrong token", 400

@app.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    result = user.create(
        username=body['username'],
        password=body['password']
    )
    if result:
        return jsonify(result)
    return "Error in registration", 400


@app.route('/measurements/<id>', methods=['GET'])
def find_measurement(id):
    if not authorize():
        return "Forbidden", 403
        
    result = measurement.find(id)
    if result:
        return jsonify(result)
    return 'Did not find measurement by id', 404


@app.route('/measurements', methods=['GET'])
def get_measurements():
    found_user = authorize()
    if not found_user:
        return "Forbidden", 403
    return jsonify(measurement.find_metas(found_user['id']))


@app.route('/measurements', methods=['POST'])
def add_measurement():
    found_user = authorize()
    if not found_user:
        return "Forbidden", 403

    body = request.get_json()
    calculated_data = utils.calculate(
        calib_data=body['calib_data'],
        throw_data=body['throw_data'],
        start_ts=body['start_ts'],
        end_ts=body['end_ts'],
        calib_start_ts=body['calib_start_ts'],
        calib_end_ts=body['calib_end_ts']
    )
    created = measurement.create(
        user_id=found_user['id'], 
        title=body['title'],
        calib_data=body['calib_data'],
        throw_data=body['throw_data'],
        start_ts=body['start_ts'],
        end_ts=body['end_ts'],
        calib_start_ts=body['calib_start_ts'],
        calib_end_ts=body['calib_end_ts'],
        velocity=calculated_data['velocity'],
        angle=calculated_data['angle']
    )
    if created:
        return jsonify(created)
    return "Error creating measurement", 400