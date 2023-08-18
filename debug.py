import pandas as pd
import requests
import os
from concurrent.futures import ThreadPoolExecutor

data = pd.read_parquet("PexelVideos.parquet.gzip")

# check data
print(data.iloc[26083]["title"])
