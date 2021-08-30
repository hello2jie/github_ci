from flask import Flask
from flask import request
import json 
import git 
import os
import subprocess


PROJECT_DIR = ''
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
RELEASE_DIR = ''

def prepare():
    g = git.cmd.Git(PROJECT_DIR)    
    g.pull()

def deploy():
    prepare()
    # cmd = ['cd', PROJECT_DIR, '&&','npm', 'run', 'build']
    cmd = ['cd', PROJECT_DIR]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in p.stdout:
        print(line)
    p.wait()
    print(p.returncode)

    
# webhook
app = Flask(__name__)

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
