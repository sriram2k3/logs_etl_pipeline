from Classes import DbLoader
from urlcheck import is_url
from Classes import *

is_valid_url, path = is_url()
if is_valid_url:
    obj = UrlLogSource(path)
    generator = obj.fetch_log()
    print("Url type source\n")
else:
    obj = FileLogSource(path)
    generator = obj.fetch_log()
    print("File type source\n")
print("Fetching Data ...\n")
collection = Collection()
for i,line in enumerate(generator, start=1):
    if not line:
        continue
    log = LogRecord(line) #parsing log

    timestamp = log.timestamp
    status = log.status
    ip = log.ip

    collection.add_log(log)  # storing log object
print("Data Fetched --> Parsed --> stored in temporary list as objects ...\n")
print(f"Top blocked ips based on occurrence :\n{collection.top_blocked_ips(5)}\n")

# database load
print("Starting to Load. Connecting to Database ...\n")
loader = DbLoader()
loader.add_data(collection.logs)
