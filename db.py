from pony.orm import *
import os
import os.path
import click
from flask.cli import with_appcontext
from datetime import datetime


db_filename = os.path.join(os.getcwd(), 'webapp', 'database.sqlite')
db = Database()

class AppUser(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    password = Required(str)
    nama_sekolah = Required(str)
    alamat_sekolah = Required(str)
    guru = Set("Guru")
    mata_pelajaran = Set("MataPelajaran")
    kelas = Set("Kelas")
    input_sch = Set("InputSch")
    SchedulerTask = Set("SchedulerTask")

class Guru(db.Entity):
    id = PrimaryKey(int, auto=True)
    app_user = Required(AppUser)
    nama = Required(str)
    nip = Required(str)
    sex = Required(str)
    input_sch = Set("InputSch")

class MataPelajaran(db.Entity):
    """docstring for ClassName"""
    id = PrimaryKey(int, auto=True)
    app_user = Required(AppUser)
    nama = Required(str)
    jpm = Required(int)
    input_sch = Set("InputSch")

class InputSch(db.Entity):
    id = PrimaryKey(int, auto=True)
    app_user = Required(AppUser)
    mata_pelajaran = Required(MataPelajaran)
    guru = Required(Guru)
    jam = Required(int)

class Kelas(db.Entity):
    id = PrimaryKey(int, auto=True)
    app_user = Required(AppUser)
    nama = Required(str)

class SchedulerTask(db.Entity):
    id = PrimaryKey(int, auto=True)
    app_user = Required(AppUser)
    status = Required(str)
    created_at = Optional(datetime, default=datetime.now)
    started_at = Optional(datetime)
    end_at = Optional(datetime)
    args = Optional(Json)
    result = Optional(Json)

# @click.command("init_db")
# @with_appcontext
def init_database():
    print('initialize database')

    db.bind(provider='sqlite', filename=db_filename, create_db=False)
    # print('bind')

    # db.create_tables()
    # print('create_tables')

    gen_res = db.generate_mapping(create_tables=True)
    # print('generate_mapping')
    # print(gen_res)

