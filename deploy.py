from flask import Flask
from flask import request
import json 
from fabric.api import cd, run
import os

app = Flask(__name__)

PROJECT_DIR = ''
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
RELEASE_DIR = ''

def deploy():
    with cd(PROJECT_DIR):
        run("git pull")
        run("")

@app.route('/ci', methods = ['POST'])
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
