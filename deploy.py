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


def prepare(tag):
    print("start clone")
    git.Repo.clone_from(url=REPO_URL, to_path=PROJECT_DIR)
    os.chdir(PROJECT_DIR)
    subprocess.call(f"git checkout tags/{tag}")
    print("pull over.")


def build():
    print("start build...")
    os.chdir(PROJECT_DIR)
    subprocess.call(
        f"npm install && npm run build && cp {DIST_DIR}/* -rf {RELEASE_DIR}", shell=True)


def clean():
    if os.path.isdir(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)


def deploy(tag):
    clean()
    prepare(tag)
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
        if ref.startswith('refs/tags'):
            tag = ref.split("/")[-1]
            if base_ref == 'refs/heads/dev':
                print('start deploy dev')
                deploy(tag)
            else:
                print('start deploy test')
                deploy(tag)
        else:
            print('ignore commit')
    return 'ok'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    deploy()
