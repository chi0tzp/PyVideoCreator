# PyVideoCreator: Create video in Python using OpenCV

A simple Python script for creating video files from images in given directory (and all its sub-directories) using OpenCV. 

## Installation

We recommend installing the required packages using python's native virtual environment as follows:

```bash
$ python -m venv py-video-creator-venv
$ source py-video-creator-venv/bin/activate
(py-video-creator-venv) $ pip install --upgrade pip
(py-video-creator-venv) $ pip install -r requirements.txt
```

## Usage

~~~
python create_video.py -h
usage: Create video from images in directory [-h] [-v] --img_dir IMG_DIR [--fps FPS] [--fourcc {MJPG,XVID}] [--video VIDEO]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  --img_dir IMG_DIR     set input image directory
  --fps FPS             set output video fps
  --fourcc {MJPG,XVID}  set the 4-character code of codec used to compress the frames.For a full set of codecs, see: http://www.fourcc.org/codecs.php
  --video VIDEO         set output video file in format <filename>.<ext>
~~~

