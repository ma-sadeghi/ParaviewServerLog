import os
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output, run
from flask import Flask, render_template


def run_shell_script(fname):
    session = Popen([fname], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception(f"Error {stderr}")
    return stdout.decode('utf-8')


def run_shell_script2(script):
    stdout = check_output([script]).decode('utf-8')
    return stdout


def is_service_running(name):
    bash_command = f"service {name} status | grep -o 'active (running)'"
    out = run(bash_command, shell=True, capture_output=True).stdout.decode('utf-8')
    status = True if out.strip() == "active (running)" else False
    return status


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET',])
def home():
    service_names = ["pvserver1", "pvserver2", "pvserver3"]
    flags = [is_service_running(name) for name in service_names]
    statuses = ["available" if flag else "in-use" for flag in flags]
    colors = ["green" if flag else "red" for flag in flags]
    out = render_template(
        "./template.html",
        statuses=statuses,
        colors=colors
    )
    return out

if __name__ == "__main__":
    app.run(debug=True)
