'''
@Version: 0.0.1
@Author: ider
@Date: 2019-08-10 16:55:38
@LastEditors: ider
@LastEditTime: 2019-08-11 22:06:28
@Description: 压缩 图片和 html
'''
from bs4 import BeautifulSoup
import base64
from PIL import Image
import io
import os

Image.MAX_IMAGE_PIXELS = None
IMG_REPLACE = {
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3goQDSYgDiGofgAAAslJREFUOMvtlM9LFGEYx7/vvOPM6ywuuyPFihWFBUsdNnA6KLIh+QPx4KWExULdHQ/9A9EfUodYmATDYg/iRewQzklFWxcEBcGgEplDkDtI6sw4PzrIbrOuedBb9MALD7zv+3m+z4/3Bf7bZS2bzQIAcrmcMDExcTeXy10DAFVVAQDksgFUVZ1ljD3yfd+0LOuFpmnvVVW9GHhkZAQcxwkNDQ2FSCQyRMgJxnVdy7KstKZpn7nwha6urqqfTqfPBAJAuVymlNLXoigOhfd5nmeiKL5TVTV+lmIKwAOA7u5u6Lped2BsbOwjY6yf4zgQQkAIAcedaPR9H67r3uYBQFEUFItFtLe332lpaVkUBOHK3t5eRtf1DwAwODiIubk5DA8PM8bYW1EU+wEgCIJqsCAIQAiB7/u253k2BQDDMJBKpa4mEon5eDx+UxAESJL0uK2t7XosFlvSdf0QAEmlUnlRFJ9Waho2Qghc1/U9z3uWz+eX+Wr+lL6SZfleEAQIggA8z6OpqSknimIvYyybSCReMsZ6TislhCAIAti2Dc/zejVNWwCAavN8339j27YbTg0AGGM3WltbP4WhlRWq6Q/btrs1TVsYHx+vNgqKoqBUKn2NRqPFxsbGJzzP05puUlpt0ukyOI6z7zjOwNTU1OLo6CgmJyf/gA3DgKIoWF1d/cIY24/FYgOU0pp0z/Ityzo8Pj5OTk9PbwHA+vp6zWghDC+VSiuRSOQgGo32UErJ38CO42wdHR09LBQK3zKZDDY2NupmFmF4R0cHVlZWlmRZ/iVJUn9FeWWcCCE4ODjYtG27Z2Zm5juAOmgdGAB2d3cBADs7O8uSJN2SZfl+WKlpmpumaT6Yn58vn/fs6XmbhmHMNjc3tzDGFI7jYJrm5vb29sDa2trPC/9aiqJUy5pOp4f6+vqeJ5PJBAB0dnZe/t8NBajx/z37Df5OGX8d13xzAAAAAElFTkSuQmCC':'data:image/webp;base64,UklGRugAAABXRUJQVlA4WAoAAAAQAAAAFQAAFQAAQUxQSJIAAAABgKpt+7rmxSG6kxw6ZEskohyC+8G4NEtEtp2Gx11LW3PfvvCz2QFExATgHzYmA9+yu7+qqBl3RPScUtFNiL2wMjrRnvghAJEbKjPmFfFfAoDrmIimDmgWxP8sAdgSe5k/ImEOAPLvjOR1BtzCq9RtGsKWzKMfkoNPwVkE0j3esReKS+bYAuUh0XEQ6ppi1YN/FVZQOCAwAAAAEAMAnQEqFgAWAD/N0OBmP7Ktpzf1WAPwOYlpAAA+hWoAAP7dDjNPcsLNsI+k8AAA'
}

def compress_base64_img(data):
    img_data = base64.b64decode(data.encode('utf8'))
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
    return base64.b64encode(newio.read()).decode('utf8'), format


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
    for img in soup.select('img'):
        data = img.attrs.get('src')
        if not data or not data.startswith('data:image'):
            continue
        if data.startswith('data:image/webp;base64'):
            continue
        line = data.split(',')
        data, format = compress_base64_img(line[1])
        img.attrs['src'] = 'data:image/'+format+';base64,'+data
    ret_data = str(soup)
    for k,v in IMG_REPLACE.items():
        ret_data = ret_data.replace(k,v)
    if len(ret_data):
        with open(file_path,'wt')as f:
            f.write(ret_data)
    return file_path

if __name__ == '__main__':
    print(compress('/tmp/cccc/img-3-3.png'))
    print(compress('/tmp/cccc/temp.html'))
    # print(compress('/home/ider/Downloads/tmp/cc.html'))
    print(compress('/home/ider/Downloads/tmp/large.png'))

    
