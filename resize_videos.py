import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

def process_video(filename, index):
    if os.path.exists(f"{video_directory}/{index}.mp4"):
        print(f"Skipping {index}")
        return
    # Get video dimensions
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout = str(result.stdout, "utf-8")
    width, height = map(int, stdout.split('\n')[:-1])

    # Compute the new dimensions and cropping parameters
    if width > height:
        new_width = int(256 * width / height)
        new_height = 256
        crop_params = f"{new_width-256}/2"
    else:
        new_width = 256
        new_height = int(256 * height / width)
        crop_params = f"{new_height-256}/2"

    output_filename = f"{video_directory}/{index}.mp4"

    print(f"Processing {output_filename}")

    # Use FFmpeg to scale the video to new dimensions, and center crop
    command = [
        "ffmpeg",
        "-y",
        "-i",
        filename,
        "-vf",
        f"scale={new_width}:{new_height},crop=256:256:{crop_params}",
        "-c:v",
        "libx264", # Use libx264 to re-encode as copy codec will not work with filter
        "-c:a",
        "copy",
        "-preset",
        "ultrafast", # Faster preset
        output_filename,
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

source_directory = "pexels"
video_directory = "pexels_processed"
os.makedirs(video_directory, exist_ok=True)

files = os.listdir(source_directory)

with ThreadPoolExecutor(max_workers=36) as executor:
    for filename in files:
        if filename.endswith(".mp4") and "chunk" not in filename:
            index = filename.split(".")[0]
            full_path = os.path.join(source_directory, filename)
            executor.submit(process_video, full_path, index)