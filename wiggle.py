
import time
import math
import subprocess
from pathlib import Path
import shutil

import pyautogui as pa

def circle_of_points(count, radius):
    points = []

    theta_spacing = 2 * math.pi / count

    for point_number in range(count):
        theta = theta_spacing * point_number
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((x, y))

    return points



frame_folder = Path(__file__).parent.joinpath('frames')
if frame_folder.exists():
    shutil.rmtree(frame_folder)
frame_folder.mkdir()

time.sleep(5)

start = pa.position()

count = 12
radius = 4

circle = circle_of_points(count, radius)
first_point = circle[0]
pa.moveTo(start[0] + first_point[0], start[1] + first_point[1])

for frame, (x, y) in enumerate(circle[1:]):
    pa.screenshot(frame_folder.joinpath(f'frame_{frame}.png'))

    pa.dragTo(start[0] + x, start[1] + y, button='middle')

    time.sleep(0.1)

pa.screenshot(frame_folder.joinpath(f'frame_{frame + 1}.png'))

# https://trac.ffmpeg.org/wiki/Encode/VP9
subprocess.check_call([
    'ffmpeg',
    '-r', '60',
    '-stream_loop', '10',
    '-i', frame_folder.joinpath('./frame_%01d.png'),
    '-vf', 'scale=1920x1080',
    '-c:v', 'libvpx-vp9',
    '-b:v', '0',
    '-crf', '30',
    '-pass', '1',
    '-y',
    '-f', 'webm',
    '/dev/null'
])
subprocess.check_call([
    'ffmpeg',
    '-r', '60',
    '-stream_loop', '10',
    '-i', frame_folder.joinpath('./frame_%01d.png'),
    '-vf', 'scale=1920x1080',
    '-c:v', 'libvpx-vp9',
    '-b:v', '0',
    '-crf', '30',
    '-pass', '2',
    '-y',
    '-f', 'webm',
    './wiggle.webm'
])
