import pandas as pd
import requests
import os
from concurrent.futures import ThreadPoolExecutor


def download_video(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


data = pd.read_parquet("PexelVideos.parquet.gzip")

# Define a directory for the videos
video_directory = "pexels"
os.makedirs(video_directory, exist_ok=True)


# Function to download a single video and print details
def download_single_video(index, row):
    url = row["content_loc"]
    filename = os.path.join(video_directory, f"{index}.mp4")
    print(f"Downloading video {index}: {url}")
    download_video(url, filename)


# Use ThreadPoolExecutor to download videos in parallel
with ThreadPoolExecutor(
    max_workers=32
) as executor:  # You can adjust max_workers based on your needs
    futures = [
        executor.submit(download_single_video, index, row)
        for index, row in data.iterrows()
        if index < 10000
    ]

    # Wait for the futures to complete
    for future in futures:
        future.result()
