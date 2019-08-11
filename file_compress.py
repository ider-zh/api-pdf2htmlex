'''
@Version: 0.0.1
@Author: ider
@Date: 2019-08-10 16:55:38
@LastEditors: ider
@LastEditTime: 2019-08-11 22:06:28
@Description: 压缩 图片和 html
'''
from bs4 import BeautifulSoup
import codecs
from PIL import Image
import io
import os

Image.MAX_IMAGE_PIXELS = None

def compress_base64_img(data):
    img_data = codecs.decode(data.encode('utf8'),'base64')
    img = Image.open(io.BytesIO(img_data))
    newio = io.BytesIO()
    try:
        img.save(newio,format='webp',quality=10,lossless=False)
        format = 'webp'
    except OSError:
        # webp 不能转换的使用黑白图保存为 png
        img = img.convert('1')
        img.save(newio,format='png',quality=10,optimize=True)
        format = 'png'
    newio.seek(0)
    return codecs.encode(newio.read(),'base64').decode('utf8'), format


def compress(file_path):
    if file_path.endswith('.png'):
        return compress_png(file_path)
    elif file_path.endswith('.html'):
        return compress_html(file_path)
    return file_path

def compress_png(file_path):
    with open(file_path,'rb')as f:
        im = Image.open(f)
        try:
            new_file_path = file_path.rstrip('png') + 'webp'
            with open(new_file_path,'wb')as fp:
                im.save(fp,format='webp',quality=10,lossless=False)
        except OSError:
            with open(file_path,'wb')as fp:
                im = im.convert('1')
                im.save(fp,format='png',quality=10,optimize=True)
                new_file_path = file_path
    return new_file_path

def compress_html(file_path):
    with open(file_path,'rb')as f:
        html = f.read()
    soup = BeautifulSoup(html,'lxml')
    flag = 0
    for img in soup.select('img'):
        data = img.attrs.get('src')
        if not data or not data.startswith('data:image'):
            continue
        if data.startswith('data:image/webp;base64'):
            continue
        line = data.split(',')
        data, format = compress_base64_img(line[1])
        img.attrs['src'] = 'data:image/'+format+';base64,'+data
        flag = 1
    if flag == 1:
        with open(file_path,'wt')as f:
            f.write(str(soup))
    return file_path

if __name__ == '__main__':
    print(compress('/tmp/cccc/img-3-3.png'))
    print(compress('/tmp/cccc/temp.html'))
    # print(compress('/home/ider/Downloads/tmp/cc.html'))
    print(compress('/home/ider/Downloads/tmp/large.png'))

    