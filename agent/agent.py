import frida
import sys,time,psutil,os
from multiprocessing import Process
func=[]

import http.server,socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd()+"\\output", **kwargs)

def server():
    with socketserver.TCPServer(("0.0.0.0", 8080), Handler) as httpd:
        httpd.serve_forever()

def on_message(message, data):
    global func
    if message['type'] == 'send':
#        print(message['payload'])
        if not message['payload'] in func:
            f=open(os.getcwd()+"\\output\\exports.txt","a+")
            f.write(message["payload"]+"\n")
            f.close()
            func.append(message['payload'])
    elif message['type'] == 'error':
        print(message['stack'])
    else:
     print(message)


def run():
    
    pid=frida.spawn(sys.argv[1])
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
    frida.resume(pid)
    sys.stdin.read()




if __name__ == "__main__":
    process1 = Process(target=server)
    process1.start()
    run()