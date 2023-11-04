import frida
import sys,time,psutil
from threading import Lock, Thread
func=[]



def on_message(message, data):
    global func
    if message['type'] == 'send':
#        print(message['payload'])
        if not message['payload'] in func:
            print(message['payload'])
            func.append(message['payload'])
    elif message['type'] == 'error':
        print(message['stack'])
    else:
     print(message)


def run():
    
    pid=frida.spawn(sys.argv[1])
    session = frida.attach(pid)

    f=open("C:\\Users\\onuro\\OneDrive\\Masaüstü\\Severus\\agent\\dll_exports\\user32.dll.txt","r")
    js=f.read()
    f.close()
    f=open("C:\\Users\\onuro\\OneDrive\\Masaüstü\\Severus\\agent\\dll_exports\\kernel32.dll.txt","r")
    js+=f.read()
    f.close()
    script = session.create_script(js)


    script.on('message', on_message)
    script.load()
    frida.resume(pid)
    sys.stdin.read()

def deneme():
    print("thread2")


if __name__ == "__main__":
	thread1 = Thread(target=run,name="frida")
	thread1.start()