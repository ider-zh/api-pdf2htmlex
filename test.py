'''
@Version: 0.0.1
@Author: ider
@Date: 2019-08-10 16:39:32
@LastEditors: ider
@LastEditTime: 2019-08-10 18:17:23
@Description: 
'''
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
                      "--dest-dir", '/tmp/cc',
                    #   '/home/ider/workspace/jupyter/temp.pdf'
                      '/home/ider/Downloads/大国空巢  作者：易富贤.pdf'
                      
                      ]

try:
    subprocess.check_output(cmd,stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    raise e
