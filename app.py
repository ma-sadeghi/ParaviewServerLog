import os
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output, run
from flask import Flask, render_template, request, jsonify


def run_shell_script(fname):
    session = Popen([fname], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception(f"Error {stderr}")
    return stdout.decode('utf-8')


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


def update_pvserver_instances(instances):
    r"""Update availability based on realtime data"""
    status = {True: "available", False: "in-use"}
    for k, v in instances.items():
        is_available = is_pvserver_available(v["name"], v["port"])
        v["status"] = status[is_available]

# Our so-called "databased"
pvserver_instances = {
    0: {"name": "pvserver1", "port": 11111, "status": ""},
    1: {"name": "pvserver2", "port": 11112, "status": ""},
    2: {"name": "pvserver3", "port": 11113, "status": ""}
}
# Update availability based on realtime data
update_pvserver_instances(pvserver_instances)

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET',])
def home():
    flags = [is_pvserver_available(s, p) for s, p in pvserver_instances.items()]
    statuses = ["available" if flag else "in-use" for flag in flags]
    colors = ["green" if flag else "red" for flag in flags]
    out = render_template(
        "./template.html",
        statuses=statuses,
        colors=colors
    )
    return out


@app.route('/api/v1/resources/pvserver', methods=['GET'])
def api_id():
    r"""
    Check if an ID was provided as part of the URL.
    If ID is provided, assign it to a variable.
    If no ID is provided, display an error in the browser.
    """
    if 'port' in request.args:
        port = int(request.args['port'])
    else:
        return "Error: No port field provided. Please specify a port."

    if 'name' in request.args:
        name = request.args['name']
    else:
        return "Error: No name field provided. Please specify a name."

    result = is_pvserver_available(name, port)
    return jsonify(result)


@app.route('/api/v1/resources/pvserver/all', methods=['GET'], strict_slashes=False)
def api_all():
    r"""Fetch available pvserver instanes and return in JSON format"""
    update_pvserver_instances(pvserver_instances)
    return jsonify(pvserver_instances)


@app.route('/amin', methods=['GET'])
def api_amin():
    return "amin"


if __name__ == "__main__":
    app.run(host="127.0.0.5", debug=True)
