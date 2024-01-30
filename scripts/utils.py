from __future__ import annotations

from typing import Generator, Any, Optional, Callable

import argparse
from omegaconf import OmegaConf

from pyutils.camera import Camera, CRF
    
    
def add_image_processor_arguments(parser:argparse.ArgumentParser) -> None:
    parser.add_argument("--camera", metavar="uri", default=argparse.SUPPRESS, help="target camera uri")
    parser.add_argument("--init_ts", metavar="timestamp", default=argparse.SUPPRESS, help="initial timestamp (eg. 0, now)")
    parser.add_argument("--sync", action='store_true')
    parser.add_argument("--show", nargs='?', const='0x0', default=argparse.SUPPRESS)
    parser.add_argument("--begin_frame", metavar="number", type=int, default=argparse.SUPPRESS,
                        help="the first frame number to show. (inclusive)")
    parser.add_argument("--end_frame", metavar="number", type=int, default=argparse.SUPPRESS,
                        help="the last frame number to show. (exclusive)")
    parser.add_argument("--title", metavar="titles", default=argparse.SUPPRESS,
                        help="title message (date+time+ts+fps+frame)")
    
    parser.add_argument("--output_video", metavar="mp4 file", default=argparse.SUPPRESS,
                        help="output video file.")
    parser.add_argument("--crf", metavar='crf', choices=[name.lower() for name in CRF.names()],
                        default='opencv', help="constant rate factor (crf).")
    
    parser.add_argument("--progress", help="display progress bar.", action='store_true')