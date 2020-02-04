import os
from time import sleep, time

from async_savers import AsyncSaverZMQProducer, AsyncSaver, load_shards


if __name__ == "__main__":
    print('Make sure to run scripts/run_async_saver_worker.py first!')
    save_path = 'outs'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ip = '127.0.0.1'
    port = '5000'
    saver = AsyncSaverZMQProducer(ip, port)
    saver.start()

    data_name = 'async_saver_zmq_demo'
    saver.new_saver(data_name, AsyncSaver, save_path, data_name, save_every=5)
    sleep(0.1)

    print('Saving data')
    for i in range(11):
        saver.save(data_name, {
            'value': i,
            'time': time()
        })
        sleep(0.1)

    saver.stop_saver(data_name)
    saver.stop()

    data_path = os.path.join(save_path, data_name)
    print('This should\'ve saved 3 shards in {}'.format(data_path))

    print('Loading saved data')
    sleep(0.1)
    saved_data = load_shards(data_path)
    print(saved_data)
