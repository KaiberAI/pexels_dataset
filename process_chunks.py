import os
from concurrent.futures import ThreadPoolExecutor
import subprocess

video_directory = "pexels_chunks"
chunk_length = 4  # seconds

os.makedirs(video_directory, exist_ok=True)


def process_video(filename, index):
    # Get video duration
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    duration = float(result.stdout)

    number_of_chunks = int(duration // chunk_length)

    for chunk_number in range(number_of_chunks):
        start = chunk_number * chunk_length
        chunk_filename = f"{video_directory}/video_{index}_chunk_{chunk_number}.mp4"

        print(f"Processing {chunk_filename}")

        # Use FFmpeg to split the video without re-encoding and downsample to 540p
        command = [
            "ffmpeg",
            "-ss",
            str(start),
            "-i",
            filename,
            "-t",
            str(chunk_length),
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            chunk_filename,
        ]
        subprocess.run(command)


source_directory = "pexels"
with ThreadPoolExecutor(
    max_workers=16
) as executor:  # You can adjust max_workers based on your needs
    futures = []
    for filename in os.listdir(source_directory):
        if filename.endswith(".mp4") and "chunk" not in filename:
            index = filename.split(".")[0]
            full_path = os.path.join(source_directory, filename)
            futures.append(executor.submit(process_video, full_path, index))

    # Wait for the futures to complete
    for future in futures:
        future.result()
