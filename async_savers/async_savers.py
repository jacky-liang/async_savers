
import os
import logging
from multiprocessing import Process, Queue
try:
    from queue import Empty
except:
    from Queue import Empty
from time import time, sleep
from pickle import dump

import numpy as np
import pandas as pd
from skimage.io import imsave

from .utils import make_shard_template


class AsyncSaver(Process):

    def __init__(self, save_path, file_prefix, save_every=10, max_n_shards=6):
        super(AsyncSaver, self).__init__()
        self._save_path = save_path
        self._save_every = save_every
        self._file_prefix = file_prefix

        self._data_q = Queue()
        self._stop_q = Queue()

        self._shard_template = make_shard_template(max_n_shards)

    def run(self):
        idx = 0
        save_path = os.path.join(self._save_path, self._file_prefix)
        if not os.path.isdir(save_path):
            os.makedirs(save_path)

        data_list = []

        get_run = lambda : True
        run = get_run()
        while run:
            try:
                new_item = False
                try:
                    data = self._data_q.get_nowait()
                    data_list.append(data)
                    new_item = True
                except Empty:
                    pass

                try:
                    done = self._stop_q.get_nowait() == 'stop'
                    if done:
                        get_run = lambda : not self._data_q.empty()
                except Empty:
                    pass 

                if new_item and len(data_list) % self._save_every == 0:
                    with open(os.path.join(save_path, self._shard_template.format(idx)), 'wb') as f:
                        dump(data_list, f)

                    data_list = []
                    idx += 1

                run = get_run()
                sleep(1e-3)
            except:
                get_run = lambda : not self._data_q.empty()
                
    def save(self, data):
        self._data_q.put(data)

    def stop(self):
        self._stop_q.put('stop')
        logging.info('Waiting for {} to finish.'.format(self.__class__))
        while self.is_alive():
            sleep(1e-3)


class AsyncCSVSaver(AsyncSaver):

    def run(self):
        df = None
        save_seg = 0
        idx = 0
        start_time = time()

        if not self._file_prefix.endswith('.csv'):
            self._file_prefix = '{}.csv'.format(self._file_prefix)

        filename = os.path.join(self._save_path, self._file_prefix)

        get_run = lambda : True
        run = get_run()
        while run:
            try:
                new_item = False
                try:
                    data = self._data_q.get_nowait()

                    data['idx'] = idx
                    data['time_save'] = time() - start_time
                    if df is None:
                        df = pd.DataFrame([data])
                    else:
                        df = df.append(data, ignore_index=True)

                    idx += 1
                    new_item = True
                except Empty:
                    pass
                
                done = False
                try:
                    done = self._stop_q.get_nowait() == 'stop'
                except Empty:
                    pass

                if done or new_item and idx % self._save_every == 0:
                    if save_seg == 0:
                        df.to_csv(filename)
                    else:
                        df.to_csv(filename, mode='a', header=False)

                    df = None
                    save_seg += 1

                if done:
                    break
                run = get_run()
                sleep(1e-3)
            except:
                get_run = lambda : not self._data_q.empty()
                

class AsyncImageSaver(AsyncSaver):

    def __init__(self, *args, save_np=False, normalize=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._save_np = save_np
        self._normalize = normalize

    def run(self):
        idx = 0
        if self._save_np:
            save_path_im = os.path.join(self._save_path, self._file_prefix, 'im')
            save_path_np = os.path.join(self._save_path, self._file_prefix, 'np')
            if not os.path.isdir(save_path_im):
                os.makedirs(save_path_im)
            if not os.path.isdir(save_path_np):
                os.makedirs(save_path_np)
        else:
            save_path = os.path.join(self._save_path, self._file_prefix)
            if not os.path.isdir(save_path):
                os.makedirs(save_path)

        get_run = lambda : True
        run = get_run()
        while run:
            try:
                try:
                    im_save = self._data_q.get_nowait()

                    im_save_np = im_save.copy()
                    if self._normalize:
                        im_save = ((im_save - im_save.min()) / (im_save.max() - im_save.min()) * 255).astype(np.uint8)
                        
                    if self._save_np:
                        imsave(os.path.join(save_path_im, '{}.png'.format(idx)), im_save)
                        np.save(os.path.join(save_path_np, '{}.npy'.format(idx)), im_save_np)
                    else:
                        imsave(os.path.join(save_path, '{}.png'.format(idx)), im_save)

                    idx += 1
                except Empty:
                    pass

                done = False
                try:
                    done = self._stop_q.get_nowait() == 'stop'
                except Empty:
                    pass

                if done:
                    break
                run = get_run()
                sleep(1e-3)
            except:
                get_run = lambda : not self._data_q.empty()
