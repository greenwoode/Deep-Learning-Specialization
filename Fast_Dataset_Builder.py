import os
import random




_BASE_DIR_ = 'G:\\DATA BACKUP'

if not os.path.exists(f'{_BASE_DIR_}\\train'):
    os.rename(f'{_BASE_DIR_}\\clean_data', f'{_BASE_DIR_}\\train')
topics = os.listdir(f'{_BASE_DIR_}\\train')

if not os.path.exists(f'{_BASE_DIR_}\\test'):
    os.mkdir(f'{_BASE_DIR_}\\test')

if not os.path.exists(f'{_BASE_DIR_}\\val'):
    os.mkdir(f'{_BASE_DIR_}\\val')

_TEST_SPLIT_ = 0.15
_VAL_SPLIT_ = 0.05

for topic in topics:

    frames = os.listdir(f'{_BASE_DIR_}\\train\\{topic}\\')
    random.shuffle(frames)
    #print(frames[:25])
     
    if not os.path.exists(f'{_BASE_DIR_}\\test\\{topic}'):
        os.mkdir(f'{_BASE_DIR_}\\test\\{topic}')
        
    if not os.path.exists(f'{_BASE_DIR_}\\val\\{topic}'):
        os.mkdir(f'{_BASE_DIR_}\\val\\{topic}')
           
    train_Split = int(len(frames) * _TEST_SPLIT_)
    val_Split = int(len(frames) * _VAL_SPLIT_)
        
    for frame in frames[:train_Split]:
        os.replace(f'{_BASE_DIR_}\\train\\{topic}\\{frame}', f'{_BASE_DIR_}\\test\\{topic}\\{frame}')

    for frame in frames[train_Split:(train_Split + val_Split)]:
        os.replace(f'{_BASE_DIR_}\\train\\{topic}\\{frame}', f'{_BASE_DIR_}\\val\\{topic}\\{frame}')

    print(f'{topic} complete.')
