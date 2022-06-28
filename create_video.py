import sys
from os import walk
import os.path as osp
import argparse
import numpy as np
from PIL import Image
import cv2


# Supported image file extensions
supported_img_ext = ('.jpg', '.png')


def refresh_stdout(num_lines):
    cursor_up = '\033[F'
    erase_line = '\x1b[K'
    for _ in range(num_lines):
        sys.stdout.write(cursor_up)
        sys.stdout.write(erase_line)


def progress_updt(msg, total, progress):
    bar_length, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(bar_length * progress))
    block_symbol = u"\u2588"
    empty_symbol = u"\u2591"
    text = "\r{}{} {:.0f}% {}".format(msg, block_symbol * block + empty_symbol * (bar_length - block),
                                      round(progress * 100, 0), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def get_img_size(image_filename):
    im = Image.open(image_filename)
    return im.size[0], im.size[1]


def query(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: {}".format(default))

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def main():
    # Set up a parser for command line arguments
    parser = argparse.ArgumentParser("Create video from images in directory")
    parser.add_argument('-v', '--verbose', action='store_true', help="increase output verbosity")
    parser.add_argument('--img_dir', type=str, required=True, help="set input image directory")
    parser.add_argument('--fps', type=int, default=1, help="set output video fps")
    parser.add_argument('--fourcc', type=str, default="MJPG",
                        choices=("MJPG", "XVID"),
                        help="set the 4-character code of codec used to compress the frames."
                             "For a full set of codecs, see: http://www.fourcc.org/codecs.php")
    parser.add_argument('--video', type=str, help="set output video file in format <filename>.<ext>")
    args = parser.parse_args()

    # Check if given video file extension is supported
    video_ext = osp.splitext(args.video)[-1]
    user_confirmation = True
    # Check if given output video file exists -- Ask user's confirmation for overwriting it
    if osp.exists(args.video):
        user_confirmation = query('Output video file exists: {}\nOverwrite?'.format(args.video))
    if not user_confirmation:
        sys.exit()

    # Check if given image dir is valid
    if not osp.isdir(args.img_dir):
        raise NotADirectoryError("Input images directory is not valid: {}".format(args.img_dir))

    if args.verbose:
        print("#. Create video file from images in directory: {}".format(args.img_dir))

    # Collect all image filenames in given directory
    img_files = []
    img_widths = []
    img_heights = []
    for r, d, f in walk(args.img_dir):
        for file in f:
            # file_basename = osp.basename(file).split('.')[0]
            img_ext = osp.splitext(file)[-1]
            if img_ext in supported_img_ext:
                img_w, img_h = get_img_size(osp.join(r, file))
                img_widths.append(img_w)
                img_heights.append(img_h)
                img_files.append(osp.join(r, file))
    img_files.sort()
    
    # Write video
    max_frame_width = max(img_widths)
    max_frame_height = max(img_heights)
    frame_shape = (max_frame_width, max_frame_height)
    fourcc = cv2.VideoWriter_fourcc(*args.fourcc)
    video = cv2.VideoWriter(args.video, fourcc, args.fps, frame_shape)
    for frame_no in range(len(img_files)):
        progress_updt("  \\__.Progress", len(img_files), frame_no + 1)
        img_w = img_widths[frame_no]
        img_h = img_heights[frame_no]
        if img_w < max_frame_width or img_h < max_frame_height:
            frame = np.zeros(shape=(max_frame_height, max_frame_width, 3), dtype=np.uint8)
            y = (max_frame_height - img_h) // 2
            x = (max_frame_width - img_w) // 2
            frame[y:y+img_h, x:x+img_w] = cv2.imread(img_files[frame_no])
        else:
            frame = cv2.imread(img_files[frame_no])
        video.write(frame)
    video.release()


if __name__ == '__main__':
    main()
