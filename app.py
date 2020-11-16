import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import Flask


def run_shell_script(fname):
    session = Popen([fname], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception(f"Error {stderr}")
    return stdout.decode('utf-8')

def run_shell_script2(fname):
    stdout = check_output([fname]).decode('utf-8')
    return stdout

app = Flask(__name__)

@app.route('/', methods=['GET',])
def home():
    fname = "./run_pvserver.sh"
    run_shell_script(fname)

if __name__ == "__main__":
    app.run(debug=True)
