from flask import (Blueprint, request, jsonify)
from webapp.api.bp import api
from pony.orm import (db_session, commit)
from webapp.db import (InputSch, Guru, MataPelajaran, AppUser,  db)
import pony

@api.route('/input_sch', methods=['GET'])
@db_session
def find_input_sch():
    id_app_user = int(request.args['id_app_user'])
    items = db.select(f"""
            isch.id as id,
            mp.nama as mp_nama,
            mp.id as mp_id,
            g.id as guru_id,
            g.nama as guru_nama,
            isch.jam as jam
        from InputSch as isch
            left join MataPelajaran as mp on isch.mata_pelajaran = mp.id
            left join Guru as g on isch.guru = g.id
        where isch.app_user = {id_app_user}
    """)
    items = [ {
        'id': it.id,
        'guru_id': it.guru_id,
        'guru_nama': it.guru_nama,
        'mp_id': it.mp_id,
        'mp_nama': it.mp_nama,
        'jam': it.jam
    } for it in items ]
    # items = pony.orm.select(
    #     { 
    #         "id": isch.id, 
    #         "mp_nama": mp.nama,
    #         "mp_id": mp.id,
    #         "guru_nama": g.nama,
    #         "guru_id": g.id
    #     }
    #     for g in Guru
    #     for mp in MataPelajaran
    #     for isch in InputSch 
    #     if (isch.app_user.id == id_app_user) and ((isch.mata_pelajaran == mp) and (isch.guru == g)))[:]
    print(items)
    # items = [ it.to_dict() for it in items ]
    return jsonify(items)

@api.route('/input_sch/<int:id_input_sch>', methods=['GET'])
@db_session
def find_input_sch_by_id(id_input_sch):
    isch = InputSch[id_input_sch]
    return jsonify(isch.to_dict())

@api.route('/input_sch', methods=['POST'])
@db_session
def create_input_sch():
    payload = request.json
    id_app_user = int(request.args['id_app_user'])
    id_guru = int(payload['id_guru'])
    id_mp = int(payload['id_mata_pelajaran'])
    app_user = AppUser[id_app_user]
    guru = Guru[id_guru]
    mp = MataPelajaran[id_mp]
    isch = InputSch(
        app_user=app_user,
        mata_pelajaran=mp,
        guru=guru,
        jam=payload['jam']
    )
    commit()
    return jsonify(isch.to_dict())

@api.route('/input_sch/<int:id_input_sch>', methods=['PUT'])
@db_session
def update_input_sch(id_input_sch):
    isch = InputSch[id_input_sch]
    payload = request.json
    isch.jam = payload['jam']
    commit()
    return jsonify(isch.to_dict())

@api.route('/input_sch/<int:id_input_sch>', methods=['DELETE'])
@db_session
def delete_input_sch(id_input_sch):
    pony.orm.delete(isch for isch in InputSch if isch.id == id_input_sch)
    commit()
    return 'OK'

