import os
from dotenv import load_dotenv
from urllib.parse import urlparse
load_dotenv()
path = os.getenv("SOURCE_PATH")
url = urlparse(path)
def is_url():
    if url.scheme == "https" or url.scheme == "http":
        return (True, path)
    else:
        return (False, path)