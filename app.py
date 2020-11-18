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


def is_port_busy(number):
    bash_command = f"netstat -nputw | grep {number}"
    out = run(bash_command, shell=True, capture_output=True).stdout.decode('utf-8')
    status = True if f"{number}" in out else False
    return status


def is_pvserver_available(service_name, port_number):
    status_service = is_service_running(service_name)
    status_port = not is_port_busy(port_number) 
    return status_service and status_port


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET',])
def home():
    services = ["pvserver1", "pvserver2", "pvserver3"]
    ports = [11111, 11112, 11113]
    flags = [is_pvserver_available(s, p) for s, p in zip(services, ports)]
    statuses = ["available" if flag else "in-use" for flag in flags]
    colors = ["green" if flag else "red" for flag in flags]
    out = render_template(
        "./template.html",
        statuses=statuses,
        colors=colors
    )
    return out

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
