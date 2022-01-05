import os
import os.path
import subprocess
from subprocess import CalledProcessError
import json
from json import JSONDecodeError

app_id= '944011620'

output = subprocess.run(['node', 'store_scraper_ios/singleRevRequest.js', app_id], stdout=subprocess.PIPE)

print(output)
