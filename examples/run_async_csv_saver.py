import os
from time import sleep, time

import pandas as pd
from async_savers import AsyncCSVSaver


if __name__ == "__main__":
    save_path = 'outs'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    data_name = 'async_saver_csv_demo.csv'
    saver = AsyncCSVSaver(save_path, data_name, save_every=5)
    saver.start()

    print('Saving data')
    for i in range(11):
        saver.save({
            'value': i,
            'time': time()
        })
        sleep(0.1)
    saver.stop()

    data_path = os.path.join(save_path, data_name)
    print('This should\'ve saved a csv file in {}'.format(data_path))

    print('Loading saved data')
    saved_data = pd.read_csv(data_path)
    print(saved_data)
