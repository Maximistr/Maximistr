import subprocess
import time
import os

# This forces all Microsoft Edge windows to close

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
process = subprocess.Popen([edge_path, "https://www.bing.com"])

# Wait for 5 seconds (as an example)
time.sleep(5)

