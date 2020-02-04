import logging
from multiprocessing import Process, Queue

from simple_zmq import SimpleZMQProducer, SimpleZMQCollector


class AsyncSaverZMQWorker(Process):

    def __init__(self, ip, port):
        super().__init__()
        self._ip = ip
        self._port = port

    def run(self):
        self._col = SimpleZMQCollector(self._ip, self._port)
        self._savers = {}

        while True:
            try:
                msg = self._col.get()
                cmd, name = msg['cmd'], msg['name']
                logging.info('Got cmd {} for {}'.format(cmd, name))
                if cmd == 'new':
                    self._savers[name] = msg['async_saver_class'](*msg['args'], **msg['kwargs'])
                    self._savers[name].start()
                elif cmd == 'save':
                    self._savers[name].save(msg['data'])
                elif cmd == 'stop_saver':
                    self._savers[name].stop()
                    self._savers.pop(name, None)
                else:
                    logging.warn('Unknown cmd!')
            except Exception as e:
                logging.warn('Got exception {}'.format(e))


class AsyncSaverZMQProducer(Process):

    def __init__(self, worker_ip, worker_port):
        super().__init__()
        self._ip = worker_ip
        self._port = worker_port

        self._q = Queue()
        self._saver_names = set()

    def run(self):
        self._prod = SimpleZMQProducer(self._ip, self._port)

        c = 0
        while True:
            msg = self._q.get()
            if msg['cmd'] == 'stop':
                break
            self._prod.push(msg)
            c += 1

    def new_saver(self, name, async_saver_class, *saver_args, **saver_kwargs):
        if name in self._saver_names:
            raise ValueError('Saver name {} already exists!'.format(name))
        self._saver_names.add(name)

        self._q.put({
            'cmd': 'new',
            'name': name,
            'async_saver_class': async_saver_class,
            'args': saver_args,
            'kwargs': saver_kwargs
        })

    def save(self, name, data):
        if name not in self._saver_names:
            raise ValueError('Saver with name {} has not been instantiated! Call new_saver first!'.format(name))

        self._q.put({
            'cmd': 'save',
            'name': name,
            'data': data
        })

    def stop_saver(self, name):
        if name not in self._saver_names:
            raise ValueError('Saver with name {} has not been instantiated! Call new_saver first!'.format(name))
        self._saver_names.remove(name)

        self._q.put({
            'cmd': 'stop_saver',
            'name': name
        })

    def stop(self):
        self._q.put({
            'cmd': 'stop'
        })