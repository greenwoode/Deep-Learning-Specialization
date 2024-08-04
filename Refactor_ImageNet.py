import numpy as np
import os
import random


N = 150
k = int(1300)

_TEST_SPLIT_ = 0.15
_VAL_SPLIT_ = 0.05

_BASE_ = 'G:\\Capstone\\Imagenet'

_LOCATION_ = f'{_BASE_}\\ILSVRC\\Data\\CLS-LOC\\'
_DEST_ = f'{_BASE_}\\150_subset\\'

_MAPPINGS_ = f'{_BASE_}\\LOC_synset_mapping.txt'

mappings = dict([])
codes = []

with open(f'{_MAPPINGS_}', 'r') as m:
    lines = m.readlines()
    for line in lines:
        line = line.split(',')[0]
        code = line.split(' ')[0]
        codes.append(code)
        thing = line.removeprefix(f'{code}').strip()
        mappings[code] = thing


if not os.path.exists(f'{_DEST_}test'):
    os.mkdir(f'{_DEST_}test')
        
if not os.path.exists(f'{_DEST_}val'):
    os.mkdir(f'{_DEST_}val')
        
if not os.path.exists(f'{_DEST_}train'):
    os.mkdir(f'{_DEST_}train')

for code in codes[:N]:
    
    images = os.listdir(f'{_LOCATION_}train\\{code}')[:k]
    
    if not os.path.exists(f'{_DEST_}test\\{mappings[code]}'):
        os.mkdir(f'{_DEST_}test\\{mappings[code]}')
        
    if not os.path.exists(f'{_DEST_}val\\{mappings[code]}'):
        os.mkdir(f'{_DEST_}val\\{mappings[code]}')
        
    if not os.path.exists(f'{_DEST_}train\\{mappings[code]}'):
        os.mkdir(f'{_DEST_}train\\{mappings[code]}')

    j = len(images)

    train_Split = int(j * _TEST_SPLIT_)
    val_Split = int(j * _VAL_SPLIT_)
        
    for frame in images[:train_Split]:
        os.replace(f'{_LOCATION_}train\\{code}\\{frame}', f'{_DEST_}test\\{mappings[code]}\\{frame}')

    for frame in images[train_Split:(train_Split + val_Split)]:
        os.replace(f'{_LOCATION_}train\\{code}\\{frame}', f'{_DEST_}val\\{mappings[code]}\\{frame}')
        
    for frame in images[(train_Split + val_Split):]:
        os.replace(f'{_LOCATION_}train\\{code}\\{frame}', f'{_DEST_}train\\{mappings[code]}\\{frame}')

    print(f'{mappings[code]} complete with {j} images.')