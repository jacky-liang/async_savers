import os
from time import sleep

from async_savers import AsyncSaver, load_shards


if __name__ == "__main__":
    save_path = 'outs'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    data_name = 'async_saver_demo'
    saver = AsyncSaver(save_path, data_name, save_every=5)
    saver.start()

    print('Saving data')
    for i in range(11):
        saver.save({
            'value': i
        })
        sleep(0.1)
    saver.stop()

    data_path = os.path.join(save_path, data_name)
    print('This should\'ve saved 3 shards in {}'.format(data_path))

    print('Loading saved data')
    saved_data = load_shards(data_path)
    print(saved_data)
