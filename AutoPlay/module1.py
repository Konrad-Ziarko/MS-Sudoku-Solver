import ctypes
import os 
import random
import stat
import string
import sys.argv
 
#define kernel32 dll
kernel32 = ctypes.windll.kernel32
 
 
def getDrives():
    print "[+] Enumerating the list of current partitions"
    drivebits=kernel32.GetLogicalDrives()
    partition_list = list()
    for drives in range(1,26):
        mask=1 << drives
        if drivebits & mask:
                drive_letter='%c:\\' % chr(ord('A')+drives)
                partition_list.append(drive_letter)
                print "\t[+]Found drive: %s" % drive_letter
    return partition_list
 
def getDriveInfo(drives):
    clean_list = list()
    for dx in drives:
        t = kernel32.GetDriveTypeA(dx)
        if t == 3:
            print "\t[+] Found Fixed Drive : " , dx
            # if we have DRIVE_FIXED
            clean_list.append(dx)
        elif t == 4: # its DRIVE_REMOTE # <- this is good for viruses
            pass
        else:
            # dont append any other type of drive
            pass
    return clean_list
 
def genRandomPath(drive):
    # enumerate and return random path from the drive ( limit to 1000 possible variants for speed )
    counter = 0
    list_dirs = list()
    for dirname, dirnames, filenames in os.walk(drive):
        for nm in filenames:
            list_dirs.append(os.path.join(dirname, nm))
            counter +=1
            if counter == 1000:
                return list_dirs
            else:
                continue
 
def getRandomDrive(list_writable_drives):
    print "[+] Selecting Partition"
    size = len(list_writable_drives)
    int = random.randrange(0,size)
    return list_writable_drives[int]
 
def selectRandomPath(limit,list):
    print "[+] Choosing $PATH"
    int = random.randrange(0,limit)
    return list[int]
 
def isFileWritable(filepath):
    print "[+] Checking File Write Permission"
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IWGRP )
 
def write(file,path):
    filename,extension = str(file).split(".")
    name = ''.join(random.choice(string.ascii_uppercase + string.digits + string.lowercase) for x in range(random.randrange(4,20)))
    const = str(name)+"."+str(extension)
     
    command = "type %s > %s:%s" % (file,path,const)
    os.popen(command)
    l = str(path)+":"+str(const)
    print "[+] File Hidden In: %s" % l
 
def ADS_HIDE(FILE_PATH):
    drives =  getDrives()
    print "[+] Checking Drive Type"
    list_to_write = getDriveInfo(drives)
    drive_to_search =  getRandomDrive(list_to_write)
    print "[+] Constructing ADS"
    # first attempt to get files
    path = selectRandomPath(1000,genRandomPath(drive_to_search))
    # check permissions on the file
    if (isFileWritable(path) == True):
        print "[+] Writing to ADS"
        write(FILE_PATH,path)
    else:
        # select another path from the list 
        path = selectRandomPath(1000,genRandomPath(drive_to_search))
        print "[+] Writing to ADS"
        write(FILE_PATH,path)
     
 
 
FILE = str(sys.argv[1])
ADS_HIDE(FILE)