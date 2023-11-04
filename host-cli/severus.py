try:
    import configparser
except:
    print("there is no configparser module.\n Please install it first.\nTips:\ndebian based distros execute 'pip install configparser'\nArch based distros pacman -S python-configparser")
import os,sys
import cli,virtualmachine
import argparse,time


parser=argparse.ArgumentParser(description="Severus Sandbox")
#___________Scan Group________________
scan=parser.add_argument_group("Analyze","Analyze a file")
scan.add_argument("--analyze",help="Sets Severus mode as 'analyze'.",required=False,action="store_true")
scan.add_argument("--file",help="Path of file",required=False)
scan.add_argument("--enable-sandbox-analysis",help="The file will be sent to sandbox.",required=False,action="store_true")
scan.add_argument("--enable-ml-model",help="The file will be sanned by ML model.",required=False,action="store_true")
#___________Integration Group_________
edr_integration=parser.add_argument_group("EDR Integration","Integrate an EDR")
edr_integration.add_argument("--integrate",help="Sets Severus mode as 'integrate'",required=False,action="store_true")
edr_integration.add_argument("--edr-vendor",help="EDR Vendor (bitdefender, kaspersky, symantec etc...)",required=False)


args=vars(parser.parse_args())
print(args)


if sys.platform!="linux":
    print("Execute the script on Linux.\n Exiting...")
    sys.exit()


home=os.path.expanduser("~")
def setup():
    print("Get ready for initial setup...")
    try:
        os.mkdir(home+"/.severus")
        os.mkdir(home+"/.severus/config")
    except:
        pass
    print("~/.severus directory created...")
    vm=input("Whats your vm software?\n\n 1. VirtualBox\n 2. Vmware\n\n Please type the number.. (1,2)\n")
    if str(vm).find("2")==-1:
        vm="VirtualBox"
        if virtualmachine.check_installation(vm):
            vm_list_command=["vboxmanage","list","vms"]
            snap_list_command=["vboxmanage","snapshot","$vm_name_parameter","list"]
        else:
            print("Did you really install VirtualBox?")
            sys.exit()
    else:
        vm="Vmware"
        print("Vmware is not supported yet! Please install VirtualBox.")
        sys.exit()
    print("\n\n")
    list_of_vms=cli.execute(vm_list_command)[0]
    print(list_of_vms)
    verify_vm_name=True
    while verify_vm_name:
        vm_name=input("Please type your vm name:")
        vm_name=vm_name.replace('"','').replace("'","")
        if list_of_vms.find('"'+vm_name+'" {')>-1:
            verify_vm_name=False
    snap_list_command[snap_list_command.index("$vm_name_parameter")]=vm_name
    snap_list=cli.execute(snap_list_command)[0]
    verify_snap_name=True
    while verify_snap_name:
        if snap_list.find("does not have")==-1:
            print("\n\n"+snap_list)
            snap_name=input("Please type snapshot name...\n")
            if snap_list.find("Name: "+snap_name+" (")>-1:
                verify_snap_name=False
        else:
            print("Take a snapshot first.")
            sys.exit()
    
    print("\n\nPlease check the informations...")
    print("VM Software:",vm,"\n","Machine Name:",vm_name,"\n","Snapshot Name:",snap_name)
    verify=input("Are all the informations correct? (y/n):")
    if verify=="y":
        f=open(home+"/.severus/config/virtualmachine.conf","w")
        conf="[VM_CONFIG]\nVM_SOFTWARE="+vm+"\nVM_NAME="+vm_name+"\nVM_SNAP="+snap_name
        f.write(conf)
        f.close
        

while not os.path.exists(home+"/.severus/config/virtualmachine.conf"):
    setup()


config=configparser.ConfigParser()
config.read(home+"/.severus/config/virtualmachine.conf")

vm_software=config['VM_CONFIG']['VM_SOFTWARE']
vm_name=config['VM_CONFIG']['VM_NAME']
snap_name=config['VM_CONFIG']['VM_SNAP']


if args["file"]!=None and args["edr_vendor"]==None:
    if vm_software=="VirtualBox":
        if virtualmachine.restoresnapshot(vm_name,snap_name,vm_software)=="Success":
            if virtualmachine.startvm(vm_name,vm_software)=="Success":
                time.sleep(600)
                virtualmachine.shutdownvm(vm_name,vm_software)