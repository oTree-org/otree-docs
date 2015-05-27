import subprocess
import shlex


class CallError(Exception):

    def __init__(self, cmd, stderr, code):
        msg = "External call '{}' fail with code '{}'. Cause: '{}'".format(
            cmd, code, stderr)
        super(CallError, self).__init__(msg)
        self.cmd = cmd
        self.stderr = stderr
        self.code = code


def call(cmd):
    pcmd = shlex.split(cmd)
    p = subprocess.Popen(pcmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode:
        raise CallError(cmd, stderr, p.returncode)
    return stdout


def get_version():
    out = [
        elem for elem in call("pip show otree-core").splitlines()
        if elem.startswith("Version")][0]
    return out.split()[-1]



