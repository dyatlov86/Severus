import frida
import sys,psutil,os,configparser
from multiprocessing import Process
import http.server,socketserver,requests
func=[]

def get_the_task():
    req=requests.get('http://192.168.56.1:8080/task.ini')
    config=configparser.ConfigParser(allow_no_value=True)
    config.read_string(req.text)
    must_be_returned=[config["TASK"][var] for var in config["TASK"]]
    return must_be_returned

def get_pid(name):
    proc = filter(lambda p: p.name() == name, psutil.process_iter())
    for i in proc:
        return i.pid

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd()+"\\output", **kwargs)

def server():
    with socketserver.TCPServer(("0.0.0.0", 8080), Handler) as httpd:
        httpd.serve_forever()

def on_message(message, data):
    global func
    if message['type'] == 'send':
        if not message['payload'] in func:
            f=open(os.getcwd()+"\\output\\exports.txt","a+")
            f.write(message["payload"]+"\n")
            f.close()
            print(message['payload'])
            func.append(message['payload'])



def run():
    
    pid=get_pid(sys.argv[1])
    session = frida.attach(pid)

    f=open(os.getcwd()+"\\dll_exports\\user32.dll.txt","r")
    js=f.read()
    f.close()
    f=open(os.getcwd()+"\\dll_exports\\kernel32.dll.txt","r")
    js+=f.read()
    f.close()
    script = session.create_script(js)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()




if __name__ == "__main__":
    print(get_the_task())
    process1 = Process(target=server)
    process1.start()
    run()
