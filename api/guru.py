from flask import (Blueprint, request, jsonify)
from webapp.api.bp import api
from pony.orm import (db_session, commit)
from webapp.db import (Guru, AppUser)
import pony

@api.route('guru', methods=['POST'])
@db_session
def create_guru():
    payload = request.json
    app_user = AppUser[payload['id_app_user']]
    guru = Guru(
        nama=payload['nama'],
        app_user=app_user,
        sex=payload['sex'],
        nip=payload['nip']
    )
    # guru.flush()
    commit()
    return jsonify(guru.to_dict())

@api.route('guru', methods=['GET'])
@db_session
def find_guru():
    id_app_user = int(request.args['id_app_user'])
    items = Guru.select(lambda g: g.app_user.id == id_app_user)[:]
    items = [ it.to_dict() for it in items ]
    return jsonify(items)

@api.route('guru/<int:id_guru>', methods=['GET'])
@db_session
def find_guru_by_id(id_guru):
    guru = Guru[id_guru]
    return jsonify(guru.to_dict())

@api.route('guru/<int:id_guru>', methods=['DELETE'])
@db_session
def delete_guru(id_guru):
    pony.orm.delete(g for g in Guru if g.id == id_guru)
    commit()
    return 'OK'

@api.route('guru/<int:id_guru>', methods=['PUT'])
@db_session
def update_guru(id_guru):
    guru = Guru[id_guru]
    payload = request.json
    guru.nama = payload['nama']
    guru.nip = payload['nip']
    guru.sex = payload['sex']
    commit()
    return jsonify(guru.to_dict())

