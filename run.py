#!/home/ider/anaconda3/bin/python

import os, time, zipfile, tempfile, uuid, shutil, subprocess, json
from flask import Flask, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
bin = "/usr/local/bin/pdf2htmlEX"
ALLOWED_EXTENSIONS = set(['pdf',])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COUNT'] = 0
app.config['executor_large'] = ThreadPoolExecutor(max_workers=1)
app.config['executor_small'] = ThreadPoolExecutor(max_workers=5)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['COUNT'] = 0

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pdf2htmlEX', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or 'command' not in request.form:
            return "no file", 404
        file = request.files['file']
        command = request.form['command']
        if file.filename == '':
            return "no filename", 404

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pdf_folder_uuid =  str(uuid.uuid4())
            pdf_floder_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_folder_uuid)
            pdf_path = os.path.join(pdf_floder_path, filename)

            file.save(pdf_path)
            try:
                fp = pdf2htmlEX(pdf_path, json.loads(command))
            except Exception as e:
                return str(e),500
            finally:
                shutil.rmtree(pdf_floder_path)

            app.config['COUNT'] += 1
            return send_file(fp,as_attachment=True,attachment_filename='%s.zip'%filename.split('.')[0])
            # return "ok" + command, 200
    elif request.method == 'GET':
        return 'Completing %s document conversions'%app.config['COUNT']
    return "unknow error", 500


def pdf2htmlEX(pdf_path,command):
    out_folder_uuid =  str(uuid.uuid4())
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], out_folder_uuid)
    os.mkdir(folder_path)
    cmd = [bin,]
    if command:
        cmd.extend(command.split(' '))

    cmd.extend(['--dest-dir',folder_path,pdf_path])

    if os.path.getsize(pdf_path) > 2 * 1024 * 1024:
        ret = app.config['executor_large'].submit(subprocess.check_output, cmd)
    else:
        ret = app.config['executor_small'].submit(subprocess.check_output, cmd)
    ret.result()

    # subprocess.check_output(cmd)
    # shutil.copy(pdf_path,os.path.join(pdf_path,folder_path))

    fp = tempfile.TemporaryFile()
    with zipfile.ZipFile(fp, 'w') as myzip:
        for obj in os.walk(folder_path):
            for file_name in obj[2]:
                file_path = obj[0] + os.sep + file_name
                # 不要 png
                if file_name.endswith('.png'):
                    continue
                myzip.write(file_path,arcname=file_path.replace(folder_path,'').lstrip('/'))
    shutil.rmtree(folder_path)
    os.remove(pdf_path)
    fp.seek(0)
    return fp


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
