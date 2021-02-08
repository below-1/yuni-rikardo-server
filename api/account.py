from flask import (Blueprint, request, jsonify)
from webapp.api.bp import api
from pony.orm import db_session, select, commit
from webapp.db import AppUser

@api.route('account/register', methods=['POST'])
@db_session
def api_create_user():
    payload = request.json
    app_user = AppUser(
        username=payload['username'],
        password=payload['password'],
        nama_sekolah=payload['nama_sekolah'],
        alamat_sekolah=payload['alamat_sekolah']
    )
    commit()
    print(app_user)
    # app_user.flush()
    return jsonify(app_user.to_dict())

@api.route('account/login', methods=['POST'])
def login():
    payload = request.json
    username = payload['username']
    password = payload['password']
    app_user = select(au for au in AppUser if au.username == username and au.password == password).first()
    if not app_user:
        result = { 'message': "can't find user" }
        return result, 404
    result = app_user.to_dict()
    return jsonify(result)
