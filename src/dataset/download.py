import os
import requests
import zipfile
from tqdm import tqdm

def download_unzip() -> str:
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    zip_path = os.path.join(raw_dir, "household_power_consumption.zip")
    txt_filename = os.path.join(raw_dir, "household_power_consumption.txt")

    url = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"

    if not os.path.exists(zip_path):
        print("Downloading dataset...")
        
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='B', unit_scale=True)
        with open(zip_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                t.update(len(data))
        t.close()
        
        print("Download finished.")
    else:
        print("ZIP already exist, skipping download.")


    if not os.path.exists(txt_filename):
        print("Unzip file...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        print("Unzip finished.")
    else:
        print("TXT file already exist, skipping unzip.")

    return txt_filename