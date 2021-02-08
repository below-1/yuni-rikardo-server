from flask import (Blueprint, request, jsonify)
from webapp.api.bp import api
from pony.orm import (db_session, commit)
from webapp.db import (MataPelajaran, AppUser)
import pony

@api.route('/mp', methods=['GET'])
@db_session
def find_mata_pelajaran():
    id_app_user = int(request.args['id_app_user'])
    items = pony.orm.select(mp for mp in MataPelajaran if mp.app_user.id == id_app_user)[:]
    items = [ it.to_dict() for it in items ]
    return jsonify(items)

@api.route('/mp/<int:id_mata_pelajaran>', methods=['GET'])
@db_session
def find_mata_pelajaran_by_id(id_mata_pelajaran):
    mp = MataPelajaran[id_mata_pelajaran]
    return jsonify(mp.to_dict())

@api.route('/mp', methods=['POST'])
@db_session
def create_mata_pelajaran():
    id_app_user = int(request.args['id_app_user'])
    app_user = AppUser[id_app_user]
    payload = request.json
    mp = MataPelajaran(
        nama=payload['nama'],
        jpm=payload['jpm'],
        app_user=app_user
    )
    # mp.flush()
    return jsonify(mp.to_dict())

@api.route('/mp/<int:id_mata_pelajaran>', methods=['PUT'])
@db_session
def update_mata_pelajaran(id_mata_pelajaran):
    mp = MataPelajaran[id_mata_pelajaran]
    payload = request.json
    mp.nama = payload['nama']
    mp.jpm = payload['jpm']
    mp.flush()
    return jsonify(mp.to_dict())

@api.route('/mp/<int:id_mata_pelajaran>', methods=['DELETE'])
@db_session
def delete_mata_pelajaran(id_mata_pelajaran):
    pony.orm.delete(mp for mp in MataPelajaran if mp.id == id_mata_pelajaran)
    commit()
    return 'OK'
