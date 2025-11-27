import time
from fetcher import fetch_and_convert

while True:
    print("Scheduled update running...")
    fetch_and_convert()
    time.sleep(21600)