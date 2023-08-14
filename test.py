from decord import VideoReader
from decord import cpu
import cv2
import numpy as np
import subprocess
import os


def resize_and_save_video(input_filename, output_filename):
    # Open the video file using Decord's VideoReader
    vr = VideoReader(input_filename, ctx=cpu(0))

    # Get the total number of frames and frame shape
    num_frames = len(vr)
    frame_height, frame_width, _ = vr[0].shape

    # Determine the scaling factor
    scale = min(256 / frame_width, 256 / frame_height)

    # Compute the new dimensions
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)

    print(
        f"Resizing video from {frame_width}x{frame_height} to {new_width}x{new_height}"
    )

    # Define the codec and create VideoWriter object
    temp_output_filename = "temp.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(
        temp_output_filename, fourcc, vr.get_avg_fps(), (new_width, new_height)
    )

    # Loop through the frames, resize each one, and write it to the new file
    for i in range(num_frames):
        # Read the next frame
        frame = vr[i].asnumpy()

        # Resize the frame with the new dimensions
        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Write the frame to the new file
        out.write(resized_frame)

    # Release the VideoWriter
    out.release()

    print(f"Resized video saved to {temp_output_filename}")

    command = [
        "ffmpeg",
        "-i",
        temp_output_filename,
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "22",
        output_filename,
    ]
    subprocess.run(command)

    # Optionally, delete the temporary file
    os.remove(temp_output_filename)

    print(f"Reencoded video saved to {output_filename}")


input_filename = "/home/fsuser/ad/data/pexelvideos/pexels_chunks/video_8279_chunk_2.mp4"
output_filename = "resized_video.mp4"
resize_and_save_video(input_filename, output_filename)
