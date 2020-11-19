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


# Our so-called "databased"
pvserver_instances = {
    "pvserver1": 11111,
    "pvserver2": 11112,
    "pvserver3": 11113
}

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
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'port' in request.args:
        port = int(request.args['port'])
    else:
        return "Error: No port field provided. Please specify a port."
    
    if 'name' in request.args:
        name = request.args['name']
    else:
        return "Error: No name field provided. Please specify a name."

    # # Create an empty list for our results
    # results = []

    # # Loop through the data and match results that fit the requested ID.
    # # IDs are unique, but other fields might return many results
    # for book in books:
    #     if book['id'] == id:
    #         results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    # return jsonify(results)
    result = is_pvserver_available(name, port)
    return jsonify(result)


@app.route('/api/v1/resources/pvserver/all', methods=['GET'])
def api_all():
    results = pvserver_instances
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
