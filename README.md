# Custom Dataset Building

These scripts are used to either build a new dataset from YouTUbe, or convert the ImageNet dataset, as a format that can be used for the [model branch](https://github.com/greenwoode/Deep-Learning-Specialization/tree/TF-CNN) code. This code creates a  `./Data/` folder that it operates in.

## Requirements:

- Install [FFmpeg](https://www.ffmpeg.org/)
- Install [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Use `requirements.txt` to build a python enviroment that has the required libraries.

Utilizes latest version of [yt-dlp](https://github.com/yt-dlp/yt-dlp) through [yt-dlp-pypi](https://pypi.org/project/yt-dlp/). Errors during download are likely caused by these being out of date.

The main `Download_and_Parse.py` script utilizes the "topics" found in `topics.txt` to search YouTube for videos. Each line is treated as a new "topic", with the includes `topics.txt` being comprised of 1000 of the top rated video games to date. To build your own dataset, simply replace the contents of `topics.txt` with your desired subjects, and adjust the prompt within `Download_and_Parse.py` itself. Note that by default, the first and last 1000 frames are dropped.

- `Download_and_Parse.py`
  - Script to automatically download videos from youtube and split them into individual frames, pulling from `topics.txt`
  - Able to specify the number of topics, the number of frames, decoding frame rate, and the desired resolution.
- `Refactor_ImageNet.py`
  - Scipt that converts the ImageNet dataset into the format of `./{dataset}/{split}/{images}`.
- `Fast_Dataset_Builder.py`
  - Script that converts the output from `Download_and_Parse.py` into the format of `./{dataset}/{split}/{images}` according to a designated train/test/validation split. This version does so in-place to minimize file operations.
- `Dataset_Builder.py`
  -   Script that converts the output from `Download_and_Parse.py` into the format of `./{dataset}/{split}/{images}` according to a designated train/test/validation split.
