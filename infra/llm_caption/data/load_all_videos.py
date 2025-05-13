import os
import ffmpeg
import hashlib
import logging
from PIL import Image

logger = logging.getLogger(__name__)


def load_all_videos():
    video_paths = find_all_videos()

    for path in video_paths:
        frames = load_video(path)

        for frame in frames:
            yield frame


def find_all_videos():
    # videos have .mp4 extension
    base_path = "/app/llm_caption/data/videos"

    # yield all video paths
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".mp4"):
                yield os.path.join(root, file)

def load_video(path):
    logger.info(f"Loading video: {path}")

    metadata = {
        "frame_number": 0,
        "video_path": path,
    }

    # The id is the hash of the video path
    m = hashlib.md5()
    m.update(str(path).encode('utf-8'))

    metadata["video_id"] = m.hexdigest()

    image = load_one_frame(path, metadata)

    return [{
        "image": image,
        "metadata": metadata,
    }]

def load_one_frame(path, metadata):
    thumbnail_path = os.path.join(os.path.dirname(path), f"{metadata['video_id']}-{metadata['frame_number']}-thumbnail.png")

    if not os.path.exists(thumbnail_path):
        generate_thumbnail(path, thumbnail_path, 0.1, 800)

    # Load the image using PIL
    image = Image.open(thumbnail_path)

    return image


def generate_thumbnail(in_filename, out_filename, time, width):
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
