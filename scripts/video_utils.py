import os
import subprocess
import tempfile
import shlex


def get_ext(path):
    """
    get a filepath's extension.
    """
    _, ext = os.path.splitext(path)
    if not ext:
        return None
    if ext.startswith("."):
        ext = ext[1:]
    return ext.lower()


def get_video_duration(path):
    """
  Get the duration of a video given its path.
  """
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '{path}'"
    p = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    try:
        return float(p.strip())
    except ValueError:
        raise RuntimeError(f"Could not parse output from {cmd}, returned: {p}")


def resize_video(input_path, size=[720, 720], output_path=None):
    """
    Resize a video.
    """
    if not output_path:
        tmp_file = tempfile.mkstemp()
        output_path = f"{tmp_file[1]}.mp4"
    cmd = f"ffmpeg -i {input_path} -vf 'crop={size[0]}:{size[1]}' '{output_path}'"
    p = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    if not os.path.exists(output_path):
        raise RuntimeError(f"Could not exceute {cmd}, returned: {p}")
    return output_path


def get_thumbnail_from_video(input_path, output_path=None):
    if not output_path:
        tmp_file = tempfile.mkstemp()
        output_path = f"{tmp_file[1]}.png"
    cmd = f"ffmpeg -i '{input_path}' -vf  'thumbnail' -frames:v 1 '{output_path}'"
    p = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    if not os.path.exists(output_path):
        raise RuntimeError(f"Could not exceute {cmd}, returned: {p}")
    return output_path


def prepare_instagram_video(video_path, thumnail_path=None, size=[720, 720]):

    # calculate duration
    print(f"Calculting duration for {video_path}")
    duration = get_video_duration(video_path)

    # resize video
    print(f"Resizing {video_path} to {size}")
    tmp_video_path = resize_video(video_path, size)

    # optionally generate thumbnail
    if not thumnail_path:
        print(f"Generating thumbnail for {video_path}")
        tmp_thumbnail_path = get_thumbnail_from_video(tmp_video_path)

    return {
        "size": (size[0], size[1]),
        "duration": round(duration, 1),
        "thumbnail_data": open(tmp_thumbnail_path, "rb"),
        "video_data": open(tmp_video_path, "rb"),
    }


def load_video(path, size):
    pass
