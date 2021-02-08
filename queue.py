from multiprocessing import Process, Queue
from flask import g
from werkzeug.local import LocalProxy


def get_queue():
	wqueue = Queue()
	if 'queue' not in g:
		print('creating queue')
		g.queue = wqueue
	return g.queue


def remove_queue():
	g.queue.close()
	q.join_thread()

queue = LocalProxy(get_queue)



