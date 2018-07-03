import requests
# files = {'file': open('/home/ider/Downloads/252b71e4b944f67ee49225f7aee9dd8dfca860fb.PDF', 'rb')}
# data= {'command':'--command'}
# req = requests.post('http://localhost:5000?dd=11',files=files,data=data)
# print(req.text)

import subprocess


cmd = ["./pdf2htmlEX", "--embed-outline", "0",
                      "--embed-css", "1",
                      "--embed-font", "0",
                      "--embed-external-font", "0",
                      "--embed-image", "1",
                      "--embed-javascript", "0",
                      # "--external-hint-tool", "ttfautohint",
                      "--no-drm", "1",
                      "--dest-dir", '/tmp/cccc',
                      '/home/ider/workspace/jupyter/temp.pdf']

try:
    subprocess.check_output(cmd,stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    raise e
