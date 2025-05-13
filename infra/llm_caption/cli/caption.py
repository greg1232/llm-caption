
from llm_caption.caption.caption import caption_videos
from llm_caption.data.load_all_videos import load_all_videos

import logging

logger = logging.getLogger(__name__)

def main():
    setup_logging()

    videos = load_all_videos()

    caption_videos(videos)

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


main()


