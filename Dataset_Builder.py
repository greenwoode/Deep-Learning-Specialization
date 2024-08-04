import os
import random


topics = os.listdir(f'.\\DATA\\')

_DEST_ = '.\\Datasets\\Games'

if not os.path.exists(f'{_DEST_}\\train\\'):
    os.mkdir(f'{_DEST_}\\train\\')
if not os.path.exists(f'{_DEST_}\\test\\'):
    os.mkdir(f'{_DEST_}\\test\\')

_TEST_SPLIT_ = 0.15

for topic in topics:

    frames = os.listdir(f'.\\CLEAN_DATA\\{topic}\\')
    random.shuffle(frames)
    #print(frames[:25])
    

    if not os.path.exists(f'{_DEST_}\\train\\{topic}\\'):
        os.mkdir(f'{_DEST_}\\train\\{topic}\\')
    if not os.path.exists(f'{_DEST_}\\test\\{topic}\\'):
        os.mkdir(f'{_DEST_}\\test\\{topic}\\')
     
           
    split = int(len(frames) * _TEST_SPLIT_)

    for frame in frames[split:]:
        os.replace(f'.\\CLEAN_DATA\\{topic}\\{frame}', f'{_DEST_}\\train\\{topic}\\{frame}')
        
    for frame in frames[:split]:
        os.replace(f'.\\CLEAN_DATA\\{topic}\\{frame}', f'{_DEST_}\\test\\{topic}\\{frame}')

    print(f'{topic} complete.')
