import cli
import time
#print(len(cli.execute(["which","which"])[1]))

def check_installation(name):
    if name=="VirtualBox":
        if len(cli.execute(["which","vboxmanage"])[1])==0:
            return True
        else:
            return False

def check_network(vm_software):
    if vm_software=="VirtualBox":
        cikti=cli.execute(["vboxmanage","list","hostonlyif"])
        if len(cikti[0])==0:
            hostonlyif_cikti=cli.execute(["vboxmanage","hostonlyif","create"])
            if len(hostonlyif_cikti[0])>0:
                return "Success"
            else:
                return "Fail"

def modify_vm_network(vm_name,vm_software):
    if vm_software=="VirtualBox":
        cikti=cli.execute(["vboxmanage","modifyvm",vm_name,"--nic1","hostonly","--hostonlyadapter2","vboxnet0"])
        if len(cikti[1])>0:
            return "Fail"
        else:
            return "Success"


def startvm(vm_name,vm_software):
    if vm_software=="VirtualBox":
        cikti=cli.execute(["vboxmanage","startvm",vm_name,"--type","gui"])
    elif vm_software=="Vmware":
        pass
    if len(cikti[1])==0:
        return "Success"
    else:
        return cikti[1]

def shutdownvm(vm_name,vm_software):
    if vm_software=="VirtualBox":
        cikti=cli.execute(["vboxmanage","controlvm",vm_name,"poweroff"])
    elif vm_software=="Vmware":
        pass
    if len(cikti[1])==0:
        return "Success"
    else:
        return cikti[1]

def restoresnapshot(vm_name,vm_snapshot,vm_software):
    if vm_software=="VirtualBox":
        cikti=cli.execute(["vboxmanage","snapshot",vm_name,"restore",vm_snapshot])
    elif vm_software=="Vmware":
        pass
    print(cikti)
    if len(cikti[0])==0 and len(cikti[1])!=0:
        return cikti
    else:
        return "Success"