#!/usr/bin/env python

import argparse
import json

from video_utils import prepare_instagram_video


def main():
    parser = argparse.ArgumentParser(
        description="Prepare arguments for an instagram video")
    parser.add_argument(
        dest="path",
        type=str,
        help="the path to the video",
    )

    args = parser.parse_args()

    res = prepare_instagram_video(args.path)
    print(json.dumps(res))
  
if __name__ == "__main__":
    main()
