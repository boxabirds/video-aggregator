import argparse
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from tqdm import tqdm

# Set up argparse to handle command line arguments
parser = argparse.ArgumentParser(description="Concatenate MP4 files with captions and an optional title.")
parser.add_argument("--source", nargs="?", default="videos", help="Folder containing MP4 files. Defaults to 'videos'.")
parser.add_argument("--title", default="More OpenAI SORA demos", help="Title text for the initial title clip. Optional.")
parser.add_argument("--output", default="output_video.mp4", help="Name of the output file. Optional.")
args = parser.parse_args()

folder_path = args.source
output_resolution = (1280, 720)
output_file = args.output
title_text = args.title
title_duration = 5  # seconds

# Create the title clip
title_clip = TextClip(title_text, fontsize=70, color='white', bg_color='black', size=output_resolution)
title_clip = title_clip.set_duration(title_duration).set_pos('center')

clips = [title_clip]

# Process videos with tqdm for progress bar
for filename in tqdm([f for f in os.listdir(folder_path) if f.endswith(".mp4")], desc="Processing Videos"):
    clip = VideoFileClip(os.path.join(folder_path, filename)).resize(newsize=output_resolution)
    stem = os.path.splitext(filename)[0]
    caption = TextClip(stem, fontsize=24, color='white', stroke_color='black', stroke_width=1, font='Arial-Bold').set_duration(clip.duration).set_position(("left", "top"))
    video_with_caption = CompositeVideoClip([clip, caption])
    clips.append(video_with_caption)

final_clip = concatenate_videoclips(clips, method="compose")
final_clip.write_videofile(output_file, fps=24)
