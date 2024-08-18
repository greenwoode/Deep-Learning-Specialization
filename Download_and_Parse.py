
import pandas as pd
import numpy as np
import ffmpeg
import yt_dlp
import os
import shutil
from requests import get
from time import sleep
import multiprocessing
import platform

#############PARAMS###############

N=150 #number of topics to download

#vidN = 1 #number of videos to download for each topic

_PROMPT_ = '(TOPIC) no commentary playthrough' #promt for yt-dlp, (TOPIC) will be replaced with the topic

down_res = 720 #resolution to pass to yt-dlp.
#Note that despite it being pass per the documentation and it being accepted, I have never had success with specifying [down_res].

frame_res = '256x256' #desired frame size, must be in 'AxB' format
K = 20000 #number of kept frames
FPS = 24 #frame rate to convert videos at.

#Frames to drop, set to 1k to avoid menus and credits.
CULL_START = 1000
CULL_END = 1000

#start threades
_DOWNLOAD_  =   True
_SPLIT_     =   True
_TRIM_      =   True
_CLEAN_     =   True

_KEEP_SOURCE_VIDEO_ = False

_MAX_LEAD_ = 5 # Maximum number of topics a thread can be ahead, reduces storage usage
#since ffmpeg is already parallelized, this actuall causes significant performance gains

_BASE_LOCATION_ = 'G:\\Capstone'
##################################


topics = []
if os.path.isfile('topics.txt'):
    with open('topics.txt', 'r') as f:
        topics = [x.strip() for x in f.readlines()]
else:
    print('"topics.txt" was not found, terminating job...')
    exit(-1)

system = platform.system() #used for determining 'rm' vs 'del'
    
pad = len(str(K))

status = multiprocessing.Array('i', 1000)

if os.path.isfile('status.txt'):
    with open('status.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(status)):
            if i < len(lines):
                status[i] = int(lines[i].strip())
            else:
                status[i] = 0
else:
    for i in range(len(status)): #initialize to 0, more compact methods override the mp.Array() typing
        status[i] = 0
    with open('status.txt', 'w') as file:
        file.writelines([f'{x}\n' for x in status])


def download(arg, foldername, filename):
    options = {'S': f'res:{down_res}', 'noplaylist':'True', 'match-filter':'duration>=900 & duration<=3600', 'outtmpl':f'{_BASE_LOCATION_}\\data\\{foldername}\\VIDEO\\{filename}.%(ext)s'}
    with yt_dlp.YoutubeDL(options) as ydl:
        error = ydl.download(f"ytsearch:{arg}")
        return error

def Down(status, topics, N):
    TC = [0]*N
    for i in range(N):
        complete = False
        while not complete:
            if status[i] != 0:
                complete = True
            elif (i - _MAX_LEAD_) >= 0:
                if status[i - _MAX_LEAD_] == 1:
                    sleep(60)
                else:
                    try:
                        topic = topics[i]
                        error = download(_PROMPT_.replace('(TOPIC)', topic), topic.replace(';', '#').replace(":", " -"), TC[i])

                        TC[i] += 1
    
                        status[i] = 1
                        with open('status.txt', 'w') as file:
                            file.writelines([f'{x}\n' for x in status])
                        complete = True
                        print(f'Downloaded {topic}.')
                    
                    except:
                        print(f'Failed downloading {topic}, retrying...')
                        TC[i] += 1
                    
                        if os.path.exists(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\'):
                            if system == 'Linux':
                                os.system('rm -rf "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\')
                            elif system == 'Windows':    
                                os.system('rd /s /q "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\')
                            #shutil.rmtree(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\VIDEO\\')

                        sleep(30)
            else:
                try:
                    topic = topics[i]
                    error = download(_PROMPT_.replace('(TOPIC)', topic), topic.replace(';', '#').replace(":", " -"), TC[i])

                    TC[i] += 1
    
                    status[i] = 1
                    with open('status.txt', 'w') as file:
                        file.writelines([f'{x}\n' for x in status])
                    complete = True
                    print(f'Downloaded {topic}.')
                    
                except:
                    print(f'Failed downloading {topic}, retrying...')
                    TC[i] += 1
                    
                    if os.path.exists(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\'):
                        if system == 'Linux':
                            os.system('rm -rf "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\')
                        elif system == 'Windows':    
                            os.system('rd /s /q "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\')
                        #shutil.rmtree(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\VIDEO\\')

                    sleep(30)
                

def Split(status, topics, N):
    for i in range(N):
        complete = False
        while not complete:
                
            if status[i] == 0:
                #print(f'{topics[i]} not ready to split, waiting...')
                sleep(30)
            elif status[i] == 1:
                if (i - _MAX_LEAD_) >= 0:
                    if status[i - _MAX_LEAD_] == 2:
                        sleep(15)
                    else:
                        topic = topics[i]
        
                        vids = os.listdir(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\')
                        if not os.path.exists(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\FRAMES\\'):
                            os.mkdir(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\FRAMES\\')
        
                        for vid in vids:
                            (
                                ffmpeg
                                .input(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\VIDEO\\{vid}')
                                .filter('fps', fps=FPS)
                                .output(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\FRAMES\\{topic.replace(";", ":").replace(":", " -")}_%05d.jpg', s=frame_res, sws_flags='bilinear')
                                .overwrite_output()
                                .run()
                            )
   
                        status[i] = 2
                        with open('status.txt', 'w') as file:
                            file.writelines([f'{x}\n' for x in status])
                        complete = True
                        print(f'Split {topic}.')
                #print(f'Starting split of {topic}')
                else:
                    topic = topics[i]
        
                    vids = os.listdir(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", " -")}\\VIDEO\\')
                    if not os.path.exists(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\FRAMES\\'):
                        os.mkdir(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\FRAMES\\')
        
                    for vid in vids:
                        (
                            ffmpeg
                            .input(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\VIDEO\\{vid}')
                            .filter('fps', fps=FPS)
                            .output(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", " -").replace(":", " -")}\\FRAMES\\{topic.replace(";", ":").replace(":", " -")}_%05d.jpg', s=frame_res, sws_flags='bilinear')
                            .overwrite_output()
                            .run()
                        )
   
                    status[i] = 2
                    with open('status.txt', 'w') as file:
                        file.writelines([f'{x}\n' for x in status])
                    complete = True
                    print(f'Split {topic}.')
                    
            elif status[i] >= 2:
                complete = True
                
def Trim(status, topics, N, K):
    if not os.path.exists(f'{_BASE_LOCATION_}\\clean_data\\'):
                    os.mkdir(f'{_BASE_LOCATION_}\\clean_data\\')
    for i in range(N):
        complete = False
        while not complete:
                
            if status[i] <= 1:
                sleep(30)
            elif status[i] == 2:
                if (i - _MAX_LEAD_) >= 0:
                    if status[i - _MAX_LEAD_] == 3:
                        sleep(15)
                    else:
                        topic = topics[i]
                
                        frames = os.listdir(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\FRAMES\\')
                
                        if K <= len(frames)-(CULL_START + CULL_END):
                            num = K
                        else:
                            num = len(frames)-(CULL_START + CULL_END)

                        try:
                            gFrames = np.linspace(CULL_START, len(frames)-CULL_END, num).astype(int)
                        except: #TOO Few Frames, use them all
                            gFrames = np.arange(len(frames))
                            
                        if not os.path.exists(f'{_BASE_LOCATION_}\\clean_data\\{topic.replace(";", "#").replace(":", "#")}\\'):
                            os.mkdir(f'{_BASE_LOCATION_}\\clean_data\\{topic.replace(";", "#").replace(":", "#")}\\')
                  
                        m = 0    
                        for j in gFrames:
                            os.replace(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\FRAMES\\{frames[j]}', f'{_BASE_LOCATION_}\\clean_data\\{topic.replace(";", "#").replace(":", "#")}\\{str(m).zfill(pad)}.jpg')
                            m += 1

                   
                        status[i] = 3
                        with open('status.txt', 'w') as file:
                            file.writelines([f'{x}\n' for x in status])
                
                
                        complete = True
                
                        print(f'Trimmed {topic}.')
                else:
                    
                    topic = topics[i]
                
                    frames = os.listdir(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\FRAMES\\')
                
                    if K <= len(frames)-(CULL_START + CULL_END):
                        num = K
                    else:
                        num = len(frames)-(CULL_START + CULL_END)

                    gFrames = np.linspace(CULL_START, len(frames)-CULL_END, num).astype(int)
                    if not os.path.exists(f'{_BASE_LOCATION_}\\clean_data\\{topic.replace(";", "#").replace(":", "#")}\\'):
                        os.mkdir(f'{_BASE_LOCATION_}\\clean_data\\{topic.replace(";", "#").replace(":", "#")}\\')
                  
                    m = 0    
                    for j in gFrames:
                        os.replace(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\FRAMES\\{frames[j]}', f'{_BASE_LOCATION_}\\clean_data\\{topic.replace(";", "#").replace(":", "#")}\\{str(m).zfill(pad)}.jpg')
                        m += 1

                   
                    status[i] = 3
                    with open('status.txt', 'w') as file:
                        file.writelines([f'{x}\n' for x in status])
                
                
                    complete = True
                
                    print(f'Trimmed {topic}.')
            elif status[i] >= 3:
                complete = True

def Clean(status, topics):
    for i in range(N):
        complete = False
        while not complete:
                
            if status[i] <= 2:
                sleep(30)
            elif status[i] == 3:
                topic = topics[i]
                if not _KEEP_SOURCE_VIDEO_:
                    if os.path.exists(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\VIDEO\\'):
                        if system == 'Linux':
                            os.system('rm -rf "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\VIDEO\\')
                        elif system == 'Windows':    
                            os.system('rd /s /q "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\VIDEO\\')
                        #shutil.rmtree(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\VIDEO\\')
                if os.path.exists(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", "#").replace(":", "#")}\\FRAMES\\'):
                    if system == 'Linux':
                        os.system('rm -rf "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", "#").replace(":", "#")}\\FRAMES\\')
                    elif system == 'Windows': 
                        os.system('rd /s /q "%s"' % f'{_BASE_LOCATION_}\\data\\{topic.replace(";", "#").replace(":", "#")}\\FRAMES\\')
                    #shutil.rmtree(f'{_BASE_LOCATION_}\\data\\{topic.replace(";", ":").replace(":", "#")}\\FRAMES\\')


                   
                status[i] = 4
                with open('status.txt', 'w') as file:
                    file.writelines([f'{x}\n' for x in status])
                                     
                complete = True
                
                print(f'Cleaned {topic}.')
            elif status[i] == 4:
                complete = True


if __name__ == "__main__": 
    
    print(f'Attempting to download {N} topics using prompt:\n{_PROMPT_}\n')

    if _DOWNLOAD_:
        print('Starting Downloader thread...')
        downloading = multiprocessing.Process(target=Down, args=(status, topics, N))
        downloading.start()
        
    if _SPLIT_:
        print('Starting Splitting worker...')
        splitting = multiprocessing.Process(target=Split, args=(status, topics, N))
        splitting.start()
        
    if _TRIM_:
        print('Starting Trimming...')
        trimming = multiprocessing.Process(target=Trim, args=(status, topics, N, K))
        trimming.start()
        
    if _CLEAN_:
        print('Starting Cleaner...')
        cleaning = multiprocessing.Process(target=Clean, args=(status, topics))
        cleaning.start()
    

    cleaning.join()
    