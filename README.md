
**Pexel Videos**

*358,551 video urls, average length 19.5s, and associated metadata from pexels.com.*

Data was extracted from their video sitemaps (pexels.com/robots.txt) on 01/08/2022.

Data is stored in PexelVideos.parquet.gzip as a gzipped parquet

Instructions:
1. Clone this repo
2. Download the parquet gzip file which stores records for all videos to the base directory: `wget https://huggingface.co/datasets/Corran/pexelvideos/resolve/main/PexelVideos.parquet.gzip`
3. Install ffmpeg: `conda install ffmpeg`
4. Install python dependencies `pip install -r requirements.txt`
5. Download 10,000 videos (total # is editable in the script): `python pexels.py`
6. Split videos into chunks of 4s (total # is editable in script): `python process_chunks.py`
7. Set the pexels_chunks folder as the training data source for your training.
