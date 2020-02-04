import os
from pickle import load, UnpicklingError


def make_shard_template(n):
    return 'shard_{:0' + str(n) + 'd}.pkl'


def load_shards(data_dir, max_n_shards=6):
    shard_template = make_shard_template(max_n_shards)
    n_shards = len(os.listdir(data_dir))
    
    data = []
    for i in range(n_shards):
        fp = os.path.join(data_dir, shard_template.format(i))
        try:
            with open(fp, 'rb') as f:
                seg = load(f)
        except (UnicodeDecodeError, UnpicklingError):
            with open(fp, 'rb') as f:
                seg = load(f, encoding='latin1')
        data.extend(seg)
    
    return data