# dynamic-vm-backup

This app does the following:
  1. Everyday at 1AM, it stops the virtual machines you requested
  2. Clones the virtual machine you requested and saves them into the backup folder with the format Date_VmName
  3. Starts the virtual machines
  4. Copies today's and yesterday's backups to the FTP
  5. Deletes backups older than one day from the local folder

As you probably know, you need to put it inside your crontab (as the running user and not root) using the following format:
```
0 1 * * * /usr/local/dynvmbkp/Main.py
```

To make your app more dynamic, we prepared a mandatory Config.xml in which you enter all the names and addresses:
  1. Please add all the virtual machines you want in:
```
<machines>
    <vm name="enter the vm name here"/>
    <vm name="enter the vm name here"/>
    <vm name="enter the vm name here"/>
    <vm name="enter the vm name here"/>
    <vm name="enter the vm name here"/>
</machines>
```
  2. Please add the local backup folder you want all the virtual machines to be saved:
```
<local>
    <backup path="/tmp/vm_backups"/>
</local>
```
  3. Please add your FTP server details in (ip address, user, password, remote path (**mandatory and should exist**) in ftp):
```
<remote>
    <machine ip="127.0.0.1" user="root" pass="123456" path="/usr/local/vm_backups"/>
</remote>
```
