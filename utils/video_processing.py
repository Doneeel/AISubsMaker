from utils.recognizer import Recognizer
from utils.subtitles_processing import process_subs
import moviepy.editor as mp

from uuid import uuid4
from typing import List, Dict
import os


def _generate_subclips(subs: List[Dict], video: mp.VideoFileClip) -> List[mp.VideoClip]:
    """
        Generate a list of subclips from a list of subtitles and a video
    """
    subclips = []
    for chunk in subs:
        duration = chunk['timestamp'][1] - chunk['timestamp'][0]
        txt_clip = mp.TextClip(chunk['text'], fontsize = 40, color = 'yellow', stroke_color='black', stroke_width=1, font='Segoe-UI-Bold') \
                    .set_duration(duration) \
                    .set_position(('center', 'bottom'))
                    
        subclip = video.subclip(*chunk['timestamp'])
        subclip = mp.CompositeVideoClip([subclip, txt_clip])
        subclips.append(subclip)
    
    return subclips

def process_video(video_path: str) -> str:
    """
        Processes a video file and returns the path to the processed video.
    """
    video = mp.VideoFileClip(video_path)

    uuid = uuid4()
    sound_filename = f"{uuid}.mp3"
    result_path = f"{uuid}.mp4"
    video.audio.write_audiofile(sound_filename)

    with Recognizer() as recognizer:
        raw_subs = recognizer.recognize(sound_filename)
        processed_subs = process_subs(raw_subs)

    subclips = _generate_subclips(processed_subs, video)
                
    mp.concatenate_videoclips(subclips) \
    .write_videofile(result_path)

    os.remove(sound_filename)

    return result_path