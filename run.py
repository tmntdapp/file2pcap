# author stanley_hsu 2023/12/4

import os
import time
import pathlib

main_command = r'sudo find / -type f -exec file {} + | grep ELF > ELF.list'

os.system("sudo apt-get install git gcc make libz-dev")
os.system("yum install git gcc make zlib-devel")
os.system("sudo dnf install git gcc make zlib-devel")
os.system("sudo zypper install git gcc make zlib-devel")
os.system("rm -rf root")

if not os.path.exists("file2pcap"):
    os.system("make")

if os.path.exists("file2pcap"):
    os.system("chmod 777 file2pcap")
else:
    print("Error: Can't make file2pcap")
    exit(1)
    
if not os.path.exists("ELF.list"):
    os.system(main_command)
    os.system("cat ELF.list")
    
if not os.path.exists('root'): os.makedirs('root')

root_path = "./root"

with open("ELF.list", 'r') as ELF:
    lines = ELF.readlines()

"https://stackoverflow.com/questions/21170795/proc-kcore-file-is-huge"

count = 0
with open("LOG.log", 'w+') as f:
    for org_file in lines:
        count+=1
        if count%2000 == 0:
            time.sleep(5)
        org_file = org_file.split(":")[0].strip().replace(" ", "\ ")
        if "/proc/kcore" == org_file: continue
        if "/.snapshots" in org_file: continue
        org_folders = org_file.split("/")
        create_folder = root_path+"/".join(org_folders[_] for _ in range(len(org_folders) - 1))

        pathlib.Path(create_folder).mkdir(parents=True, exist_ok=True)
        print(f"./file2pcap {org_file} -o {root_path+org_file}.pcap")
        f.write(os.popen(f"./file2pcap {org_file} -o {root_path+org_file}.pcap").read())
os.system("cp LOG.log root")
os.system("cp ELF.list root")
os.system("tar zcvf root.tar.gz root/")
