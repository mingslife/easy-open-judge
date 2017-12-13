import sys, os, time, uuid, sqlite3

from flask import Flask
from flask import request
from flask import url_for, render_template, jsonify

project_path = sys.path[0]

# conn = sqlite3.connect('data.db')
# cursor = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/code', methods=['POST'])
def submit_code():
    global project_path

    subject_path = 'subject/1'
    
    docker_name = str(uuid.uuid1())
    temp_path = 'temp/' + docker_name
    temp_absolute_path = project_path + '/' + temp_path

    os.mkdir('{}'.format(temp_path))
    code = request.form['code']

    with open(temp_path + '/app.c', 'w') as f:
        f.write(code)

    os.system('gcc -o {0}/app {0}/app.c'.format(temp_path)) # TODO 编译报错处理
    os.system('cp {}/input.txt {}/'.format(subject_path, temp_path))
    os.system('cp {}/run.sh {}/'.format(subject_path, temp_path))
    time.sleep(1)
    os.system('docker run --name {0} -v {1}:/app centos bash /app/run.sh > {1}/output.txt'.format(docker_name, temp_absolute_path))
    # TODO 超时处理，超时程序没跑完，直接docker rm -f {docker_name}
    time.sleep(1)
    os.system('docker rm {}'.format(docker_name))

    with open(subject_path + '/output.txt', 'r') as f:
        output = f.read()[:-1] # 不知道为什么后面会多一个换行
        # print("answer: " + output)
    with open(temp_path + '/output.txt', 'r') as f:
        output_temp = f.read()
        # print("user: " + output_temp)
    os.system("rm -r {}".format(temp_path))

    if output_temp == output:
        json_dict = {'ac': True}
    else:
        json_dict = {'ac': False}

    return jsonify(json_dict)

if __name__ == '__main__':
    app.run(debug=True)

