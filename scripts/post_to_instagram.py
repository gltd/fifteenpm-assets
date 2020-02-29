#!/usr/bin/env python3

import json
import os
import codecs
import datetime
import os.path
import logging
import argparse

from video_utils import prepare_instagram_video

try:
    from instagram_private_api import (
        Client,
        ClientError,
        ClientLoginError,
        ClientCookieExpiredError,
        ClientLoginRequiredError,
        __version__ as client_version,
    )
except ImportError:
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from instagram_private_api import (
        Client,
        ClientError,
        ClientLoginError,
        ClientCookieExpiredError,
        ClientLoginRequiredError,
        __version__ as client_version,
    )


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {
            "__class__": "bytes",
            "__value__": codecs.encode(python_object, "base64").decode(),
        }
    raise TypeError(repr(python_object) + " is not JSON serializable")


def from_json(json_object):
    if "__class__" in json_object and json_object["__class__"] == "bytes":
        return codecs.decode(json_object["__value__"].encode(), "base64")
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, "w") as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print("SAVED: {0!s}".format(new_settings_file))


def parse_args():
    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(
        description="login callback and save settings demo")
    parser.add_argument(
        "-c",
        "--config",
        dest="settings_file_path",
        type=str,
        default="config/instagram-credentials.json",
        help="The path the the json file to cache your ",
    )
    parser.add_argument(
        "-u",
        "--username",
        dest="username",
        type=str,
        default=os.getenv("INSTAGRAM_USERNAME"),
        help="Your instagram username, or $INSTAGRAM_USERNAME",
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="password",
        type=str,
        default=os.getenv("INSTAGRAM_PASSWORD"),
        help="Your instagram password, or $INSTAGRAM_PASSWORD",
    ),
    parser.add_argument("-t",
                        "--caption",
                        dest="caption",
                        type=str,
                        required=True,
                        help="The caption for your album")
    parser.add_argument(
        "-m",
        "--medias",
        dest="medias",
        type=lambda p: json.load(open(p)),
        required=True,
        help="""
    A path to a json file that contains the following info
    #  [
    #     {"type": "image", "path": "path/to/image"},
    #     {"type": "video",  "path": "path/to/video" "thumbnail": "path/to/thumbnail"}
    # ]

    """,
    )
    parser.add_argument("-debug", "--debug", action="store_true")
    return parser.parse_args()


def setup_logging(args):
    logging.basicConfig()
    logger = logging.getLogger("instagram_private_api")
    logger.setLevel(logging.WARNING)
    if args.debug:
        logger.setLevel(logging.DEBUG)


def login(args):
    device_id = None
    try:

        settings_file = args.settings_file_path
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print("Unable to find file: {0!s}".format(settings_file))

            # login new
            api = Client(
                args.username,
                args.password,
                on_login=lambda x: onlogin_callback(x, args.settings_file_path
                                                    ),
            )
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print("Reusing settings: {0!s}".format(settings_file))

            device_id = cached_settings.get("device_id")
            # reuse auth settings
            api = Client(args.username,
                         args.password,
                         settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print(
            "ClientCookieExpiredError/ClientLoginRequiredError: {0!s}".format(
                e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            args.username,
            args.password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path),
        )

    except ClientLoginError as e:
        print("ClientLoginError {0!s}".format(e))
        exit(9)
    except ClientError as e:
        print("ClientError {0!s} (Code: {1:d}, Response: {2!s})".format(
            e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print("Unexpected Exception: {0!s}".format(e))
        exit(99)

    return api


def load_medias(medias):
    media_args = []
    for media in medias:
        if media['type'] == 'video':
            video_args = prepare_instagram_video(media['path'])
            media_args.append(video_args)
        elif media['type'] == 'image':
            pass
    return media_args


def main():

    print("Client version: {0!s}".format(client_version))
    args = parse_args()
    setup_logging(args)

    # Login to the API
    api = login(args)
    media_args = load_medias(args.medias)
    # print("got args")
    # print("===========================================")
    # print(media_args)
    # print("===========================================")
    kwargs = media_args[0]
    kwargs.update(caption=args.caption)
    metadata = api.post_video(video_data=kwargs['video_data'],
                               size=kwargs['size'],
                               duration=kwargs['duration'],
                               thumbnail_data=kwargs['thumbnail_data'],
                               caption=args.caption,
                               is_sidecar=True)
    print(metadata)


if __name__ == "__main__":
    main()
