import asyncio
from asyncio.subprocess import PIPE
from datetime import datetime
import sys
import time
import pprint
import os
import shutil
# main coroutine
linev=[]
def checkline(linev):
	for line in linev:
		if "already exists and is not an empty directory" in line:
			print("already exists and is not an empty directory find\n")
			return 10
		if "gnutls_handshake() failed" in line:
			print("gnutls_handshake() failed\n")
			return 11
		if "read: connection reset by peer" in line:
				print("read: connection reset by peer find")
				return 12
	return 0
async def main():
    # create a subprocess using create_subprocess_shell()
    process = await asyncio.create_subprocess_shell('git lfs clone https://huggingface.co/Phind/Phind-CodeLlama-34B-v1 Phind/Phind-CodeLlama-34B-v1', stdout=asyncio.subprocess.PIPE)
    # read data from the subprocess
    data, _ = await process.communicate()
    # report the data
    print("data=",data)
 
# entry point
async def read_stdout(process):
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        print(line.decode().strip())

async def main1():
    cmd = "git lfs clone https://huggingface.co/Phind/Phind-CodeLlama-34B-v1 Phind/Phind-CodeLlama-34B-v1"

    process = await asyncio.create_subprocess_exec(*cmd.split(), stdout=asyncio.subprocess.PIPE)
    await read_stdout(process)
async def watch(stream, prefix=''):
    async for line in stream:
        print(datetime.now(), prefix, line.decode().strip())
        linev.append(line.decode().strip())

async def run(cmd):
    p = await asyncio.create_subprocess_shell(cmd, stdout=PIPE)
    await asyncio.gather(watch(p.stdout))
    print(p.returncode)
async def run1(cmd):
    p = await asyncio.create_subprocess_shell(cmd,stderr=PIPE)
    await  asyncio.gather(watch(p.stderr,'E:'))
    print("run1",p.returncode)
    return p.returncode
async def run11(cmd):
    global linev
    linev=[]
    p = await asyncio.create_subprocess_exec(*cmd.split(),stderr=PIPE)
    await  asyncio.gather(watch(p.stderr,'E:'))
    print("run11=",p.returncode,"=")
    print("linev=",linev)
    checkstatus= checkline(linev)
    print("checkstatus=",checkstatus)
    return p.returncode,checkstatus
cmd = "git lfs clone https://huggingface.co/Phind/Phind-CodeLlama-34B-v1 Phind/Phind-CodeLlama-34B-v1"

async def run3(cmd,dest):
    global okv
    global faiv
    retry= 0
    while True:
        returncode,checkstatus = await run11(cmd)
        if returncode is None and checkstatus== 0 :
                print("returncode is none")
                return 
        else:
            if returncode == 0:
                print("clone ok")
                okv.append(cmd)
                return  
            if returncode == 10:
                 print("lfs clone fail rmmove")
                 shutil.rmtree(dest)
            print("failv")
            pprint.pprint(failv)
            time.sleep(15)
        retry= retry+1
        if retry > 150:
            failv.append(cmd)
            return 0
    return 1
repo= sys.argv[1]
dest= sys.argv[2]
cmd = f"git lfs clone {repo} {dest}"
import csv
okv=[]
failv=[]
with open("hface.csv", 'r') as file:
  csvreader = csv.reader(file, delimiter=' ')

  for row in csvreader:
    print(row)
    if row[2] == '0':
        cmd = f"git lfs clone {row[0]} {row[1]}"
        print(cmd)
        if os.path.exists(row[1]):
             failv.append(row[1])
        else:
             asyncio.run(run3(cmd,row[1]))
#asyncio.run(run3(cmd))
print("failv=")
pprint.pprint(failv)
cmd = "git lfs clone https://huggingface.co/Phind/Phind-CodeLlama-34B-v1 Phind/Phind-CodeLlama-34B-v1"

#asyncio.run(run1())

