from flask import Flask
from flask import request
import json
import git
import os
import subprocess
import shutil


# Repo
REPO_URL = "https://github.com/hello2jie/github_ci.git"
# 项目路径
PROJECT_DIR = '/home/van/github_ci'
# 编译生成路径
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
# 部署地址
RELEASE_DIR = '/home/van/front'


def prepare():
    print("start clone")
    g = git.Repo.clone_from(url=REPO_URL, to_path=PROJECT_DIR)
    print("pull over.")


def build():
    print("start build...")
    os.chdir(PROJECT_DIR)
    subprocess.call(
        f"npm install && npm run build && cp {DIST_DIR}/* -rf {RELEASE_DIR}", shell=True)


def clean():
    if os.path.isdir(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)


def deploy():
    clean()
    prepare()
    build()


# webhook
app = Flask(__name__)


@app.route('/ci', methods=['POST'])
def ci():
    payload = request.form.get('payload')
    if payload:
        payload = json.loads(payload)
        ref = payload.get('ref')
        base_ref = payload.get('base_ref')
        if ref.startswith('refs/tags') and base_ref == 'refs/heads/main':
            print('start deploy')
            deploy()
        else:
            print('ignore commit')
    return 'ok'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    deploy()
