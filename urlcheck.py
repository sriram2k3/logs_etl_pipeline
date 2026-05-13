import os
from dotenv import load_dotenv
from urllib.parse import urlparse
load_dotenv()
file_path = os.getenv("SOURCE_PATH")
url = urlparse(file_path)
def is_url():
    if url.scheme == "https" or url.scheme == "http":
        return (True, file_path)
    else:
        return (False, file_path)