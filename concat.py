#!/usr/bin/env python3

import os
import sys
from pydub import AudioSegment
from typing import List, Union


def makeAudioSegmentFromFilename(filename: str) -> AudioSegment:
    return AudioSegment.from_file(file=filename, format="raw", frame_rate=48000, channels=2, sample_width=2)

directory = sys.argv[1]
outpath = sys.argv[2]

filenameList = list(
    map(lambda file: file.path, filter(lambda child: child.is_file(), os.scandir(directory)))
)
filenameList.sort(key=lambda x: int(os.path.basename(x).replace(".pcm", "")))

audioSegments = list(map(lambda filename: makeAudioSegmentFromFilename(filename), filenameList))


merged = AudioSegment.empty()
last_msec = 0

for i in range(0, len(filenameList)):
    cr = audioSegments[i]
    cr_msec = int(os.path.basename(filenameList[i]).replace(".pcm", ""))
    print("cr_msec: ", cr_msec)
    cr_length = len(cr)
    print("cr_length: ", cr_length)
    silence_msec = cr_msec - last_msec
    print("silence_msec: ", silence_msec)
    merged += AudioSegment.silent(duration=silence_msec)
    merged += cr
    last_msec = cr_msec + cr_length

merged.export(outpath, format="ipod", codec="aac", bitrate="64K")