import os


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
