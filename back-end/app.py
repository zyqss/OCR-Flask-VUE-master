import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector

import core.main



#  上传文件到服务器指定到文件夹中(一定要放在自己起服务到那个文件夹，不要放在本地的其他文件夹中，不然服务器访问不了你的文件)
UPLOAD_FOLDER = r'./uploads'

#  上传文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.secret_key = 'secret!'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)



# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response

# 允许的图片模式为PNG或者JPG
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))


# id part
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # file是目标文件
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        # shutil.copyfileobj(文件1，文件2)：将文件1的数据覆盖copy给文件2。
        shutil.copy(src_path, './tmp/ct')
        # os.path.join()函数用于路径拼接文件路径，可以传入多个路径
        image_path = os.path.join('./tmp/ct', file.filename)
        pid, img_z, image_info, id_info = core.main.c_main(
            image_path, Detector, file.filename.rsplit('.', 1)[1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info,
                        "id_info": id_info})

    return jsonify({'status': 0})

# menu part
@app.route('/upload1', methods=['GET', 'POST'])
def upload_file1():
    # file是目标文件
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        # shutil.copyfileobj(文件1，文件2)：将文件1的数据覆盖copy给文件2。
        shutil.copy(src_path, './tmp/ct')
        # os.path.join()函数用于路径拼接文件路径，可以传入多个路径
        image_path = os.path.join('./tmp/ct', file.filename)
        pid, img_z, image_info = core.main.b_main(
            image_path, Detector, file.filename.rsplit('.', 1)[1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info})

# receipt part
@app.route('/upload2', methods=['GET', 'POST'])
def upload_file2():
    # file是目标文件
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        # shutil.copyfileobj(文件1，文件2)：将文件1的数据覆盖copy给文件2。
        shutil.copy(src_path, './tmp/ct')
        # os.path.join()函数用于路径拼接文件路径，可以传入多个路径
        image_path = os.path.join('./tmp/ct', file.filename)
        pid, img_z, image_info, receipt_info = core.main.a_main(
            image_path, Detector, file.filename.rsplit('.', 1)[1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info,
                        'receipt_info': receipt_info})
    return jsonify({'status': 0})


# ticket part
@app.route('/upload3', methods=['GET', 'POST'])
def upload_file3():
    # file是目标文件
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)

        # shutil.copyfileobj(文件1，文件2)：将文件1的数据覆盖copy给文件2。
        shutil.copy(src_path, './tmp/ct')

        # os.path.join()函数用于路径拼接文件路径，可以传入多个路径
        image_path = os.path.join('./tmp/ct', file.filename)
        pid, img_z, image_info, ticket_info = core.main.d_main(
            image_path, Detector, file.filename.rsplit('.', 1)[1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info,
                        'ticket_info': ticket_info})
    return jsonify({'status': 0})


# business part
@app.route('/upload4', methods=['GET', 'POST'])
def upload_file4():
    # file是目标文件
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)

        # shutil.copyfileobj(文件1，文件2)：将文件1的数据覆盖copy给文件2。
        shutil.copy(src_path, './tmp/ct')

        # os.path.join()函数用于路径拼接文件路径，可以传入多个路径
        image_path = os.path.join('./tmp/ct', file.filename)
        pid, img_z, image_info, business_info = core.main.e_main(
            image_path, Detector, file.filename.rsplit('.', 1)[1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info,
                        'business_info': business_info})
    return jsonify({'status': 0})



# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            # 响应的图片形式为png；content-type是响应消息报头中的一个参数，标识响应正文数据的格式
            response.headers['Content-Type'] = 'image/png'
            return response




if __name__ == '__main__':
    files = [
        'uploads', 'tmp/ct', 'tmp/draw',
    ]
    app.run(host='127.0.0.1', port=5003, debug=True)
