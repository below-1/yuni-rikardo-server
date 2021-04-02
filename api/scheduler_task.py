from webapp.api.bp import api
from webapp.db import SchedulerTask, AppUser, Kelas, InputSch, db, MataPelajaran
from flask import Blueprint, request, jsonify, g
from pony.orm import (db_session, commit, select)
import json

bobot_hari = [ { "hari": 0, "max": 7 }, { "hari": 1, "max": 8 }, { "hari": 2, "max": 8 }, { "hari": 3, "max": 7 }, { "hari": 4, "max": 5 }, { "hari": 5, "max": 5 }]

@api.route('scheduler_task', methods=['POST'])
@db_session
def create_task():
    id_app_user = int(request.args['id_app_user'])
    app_user = AppUser[id_app_user]
    payload = request.json

    kelas = select(k for k in Kelas if k.app_user == app_user)
    kelas = [ k.to_dict() for k in kelas ]

    mps = select(mp for mp in MataPelajaran if mp.app_user == app_user)
    mps = [ mp.to_dict() for mp in mps ]

    mp_guru = db.select(f"""
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
    mp_guru = [ {
        'id': it.id,
        'guru_id': it.guru_id,
        'guru_nama': it.guru_nama,
        'mp_id': it.mp_id,
        'mp_nama': it.mp_nama,
        'jam': it.jam
    } for it in mp_guru ]

    payload['kelas_list'] = kelas
    payload['mp_guru_list'] = mp_guru
    payload['mp_list'] = mps
    payload['bobot_hari'] = bobot_hari
    st = SchedulerTask(
        app_user=app_user,
        args=payload,
        status='ready',
    )
    commit()

    return jsonify(payload)

@api.route('scheduler_task', methods=['GET'])
@db_session
def list_task():
    id_app_user = int(request.args['id_app_user'])
    app_user = AppUser[id_app_user]
    items = select(t for t in SchedulerTask if t.app_user == app_user)
    items = [ t.to_dict() for t in items ]
    return jsonify(items)

@api.route('scheduler_task/<int:task_id>', methods=['GET'])
@db_session
def find_task(task_id):
    task = SchedulerTask[task_id]
    return jsonify(task.to_dict())

@api.route('scheduler_task/<int:id_task>', methods=['DELETE'])
@db_session
def remove_task(id_task):
    task = SchedulerTask[id_task]
    task.status = 'cancel'
    commit()
    return 'OK'

@api.route('try', methods=['GET'])
def just_try():
    with open('webapp/result.json') as f:
        result = json.load(f)
        return jsonify(result)
