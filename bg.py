from multiprocessing import Process, Queue
import time
import sys
from pso import pso
import foo
from pony.orm import db_session, select, commit
from db import db, SchedulerTask

all_tasks = []

def run_sch(id):
    # TURNOFF THIS ON WINDOWS
    # db.bind(provider='sqlite', filename=db_filename, create_db=False)
    # db.generate_mapping(create_tables=False)
    print("running scheduler")
    with db_session:
        task = SchedulerTask[id]
        task.status = "running"
        commit()

        n_kelas = len(task.args['kelas_list'])
        mpg = task.args['mp_guru_list']
        mp_target = { it['id']: it['jpm'] for it in task.args['mp_list'] }

        xs = foo.f(mp_target, mpg, n_kelas)
        result = foo.decode(xs)
        task.result = result
        task.status = "done"
        commit()

def remove_canceled(id):
    try:
        exist_task = next(data for data in all_tasks if data['id'] == id)
        exist_task['p'].terminate()
    except StopIteration:
        print(f"task#{id} not found")
    with db_session:
        SchedulerTask[id].delete()

def handle_task(task):
    if task['status'] == 'cancel':
        remove_canceled(task['id'])
    elif task['status'] == "ready":
        p = Process(target=run_sch, daemon=True, args=(task['id'],))
        all_tasks.append({
            'id': task['id'],
            'p': p
        })
        p.start()

def load_tasks(db):
    global all_tasks
    print('checking tasks from database')
    with db_session:
        tasks = select(st for st in SchedulerTask)[:]
        tasks = [ t.to_dict() for t in tasks ]
    db.disconnect()
    for task in tasks:
        handle_task(task)

if __name__ == '__main__':
    from db import db, db_filename
    # start database
    db.bind(provider='sqlite', filename=db_filename, create_db=False)
    # db.create_tables()
    db.generate_mapping(create_tables=False)
    while True: 
        # sleep 5 seconds
        time.sleep(2)
        # check tasks from database
        load_tasks(db)
        # for each available task:
        #   create task
        #   store reference of it
        #   run it
        #