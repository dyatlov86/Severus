import subprocess


def execute(arguments):
    ex=subprocess.run(arguments,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return ex.stdout.decode("utf-8"),ex.stderr.decode("utf-8")