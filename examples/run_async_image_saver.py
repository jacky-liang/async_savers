import os
from time import sleep, time
import numpy as np

from async_savers import AsyncImageSaver


if __name__ == "__main__":
    save_path = 'outs'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    data_name = 'async_saver_image_demo'
    saver = AsyncImageSaver(save_path, data_name, save_np=True, normalize=True)
    saver.start()

    print('Saving data')
    for _ in range(11):
        im = np.random.random((100, 100))
        saver.save(im)
        sleep(0.1)
    saver.stop()

    data_path = os.path.join(save_path, data_name)
    print('This should\'ve saved images in {}'.format(data_path))
