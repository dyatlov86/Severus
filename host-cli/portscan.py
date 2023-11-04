import socket,psutil


def get_host_ip(interface):
    interface_addr=psutil.net_if_addrs().get(interface)
    for sni in interface_addr:
        if sni.family==socket.AF_INET:
            return sni.address


def scan():
    socket.setdefaulttimeout(0.02)
    piece=get_host_ip("vboxnet0").split(".")
    ips=[ piece[0]+"."+piece[1]+"."+piece[2]+"."+str(i) for i in range(2,255)]
    for ip in ips:
        try:
            tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            if not tcp.connect_ex((ip,8080)):
                return ip
        except:
            pass
    return "Agent is not running!" 


print(scan())