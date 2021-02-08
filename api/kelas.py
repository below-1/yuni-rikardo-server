from flask import (Blueprint, request, jsonify)
from webapp.api.bp import api
from pony.orm import (db_session, commit)
from webapp.db import (Kelas, AppUser)
import pony

@api.route('kelas', methods=['GET'])
@db_session
def find_kelas():
    id_app_user = int(request.args['id_app_user'])
    items = pony.orm.select(k for k in Kelas if k.app_user.id == id_app_user)[:]
    items = [ it.to_dict() for it in items ]
    return jsonify(items)

@api.route('kelas', methods=['POST'])
@db_session
def create_kelas():
    payload = request.json
    id_app_user = int(request.args['id_app_user'])
    app_user = AppUser[id_app_user]
    kelas = Kelas(
        app_user=app_user,
        nama=payload['nama']
    )
    commit()
    # kelas.flush()
    return jsonify(kelas.to_dict())

@api.route('kelas/<int:id_kelas>', methods=['PUT'])
@db_session
def update_kelas(id_kelas):
    kelas = Kelas[id_kelas]
    payload = request.json
    kelas.nama = payload['nama']
    commit()
    return jsonify(kelas.to_dict())

@api.route('kelas/<int:id_kelas>', methods=['GET'])
@db_session
def find_kelas_by_id(id_kelas):
    kelas = Kelas[id_kelas]
    return jsonify(kelas.to_dict())

@api.route('kelas/<int:id_kelas>', methods=['DELETE'])
@db_session
def delete_kelas_by_id(id_kelas):
    pony.orm.delete(k for k in Kelas if k.id == id_kelas)
    commit()
    return 'OK'
