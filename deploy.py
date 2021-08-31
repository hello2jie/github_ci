from flask import Flask
from flask import request
import json
import git
import os
import subprocess
import shutil


# Repo
REPO_URL = "git@github.com:0xalexbai/solhedge-fe.git"
# 项目路径
PROJECT_DIR = '/home/alex/deploy/github_ci'
# 编译生成路径
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
# 部署地址
WEB_DEV_SERVICE = 'web-dev'
WEB_TEST_SERVICE = 'web-test'


def prepare(tag):
    print("start clone")
    repo = git.Repo.clone_from(url=REPO_URL, to_path=PROJECT_DIR)
    repo.git.checkout(tag)
    print("pull over.")


def build(target):
    print("start build...")
    os.chdir(PROJECT_DIR)
    subprocess.call(
        f"npm install && npm run build", shell=True)
    subprocess.call(
        f'docker-compose -f {PROJECT_DIR}/docker-compose.yaml up --build -d {target}')


def clean():
    if os.path.isdir(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)


def deploy(tag, target):
    clean()
    prepare(tag)
    build(target)


# webhook
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.form.get('payload')
    if payload:
        payload = json.loads(payload)
        ref = payload.get('ref')
        base_ref = payload.get('base_ref')
        if ref.startswith('refs/tags'):
            tag = ref.split("/")[-1]
            if base_ref == 'refs/heads/dev':
                print('start deploy dev')
                deploy(tag, WEB_DEV_SERVICE)
            else:
                print('start deploy test')
                deploy(tag, WEB_TEST_SERVICE)
        else:
            print('ignore commit')
    return 'ok'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    deploy('v1.0.3', WEB_TEST_SERVICE)
