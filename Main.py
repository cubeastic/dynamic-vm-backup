#!/usr/bin/python
from ConfigManager import ConfigManager
from VmManager import VmManager
from FtpManager import FtpManager
import os
from datetime import date, timedelta
from shutil import rmtree
from time import sleep

pattern = "%Y_%m_%d"


def backup_machine_locally(from_path, to_path, machine_bkp_name):
    os.system("\cp " + from_path + "/" + machine_bkp_name + " " + to_path + "/" + machine_bkp_name)


def deter_file_dates(file_name):
    file_name = file_name.split("_")
    file_date_str = '{0}_{1}_{2}'.format(file_name[0], file_name[1], file_name[2])
    yesterday = (date.today() - timedelta(1)).strftime(pattern)

    if file_date_str < yesterday:
        return True
    else:
        return False

if __name__ == "__main__":
    config = ConfigManager()
    config.recursive_get_xml(config.root, 0)

    # Will contain [uuid (id), machine name (name)]
    vm_list = []

    backup_path = ""
    vbox_clone_path = ""
    remote_machine = ["", "", "", ""]  # ip, user, pass, path

    # Use all the configuration data
    for hold in config.holder:
        id = ""
        name = ""
        try:
            if hold[1] == "vm":
                try:
                    id = hold[2]["id"]
                except:
                    pass
                try:
                    name = hold[2]["name"]
                except:
                    print "Unnamed machine found in config. Exiting task"
                    exit(1)

                vm_list.append([id, name])

            if hold[1] == "vbox":
                vbox_clone_path = hold[2]["clone_path"]

            if hold[1] == "backup":
                backup_path = hold[2]["path"]

            if hold[1] == "machine":
                remote_machine[0] = hold[2]["ip"]
                remote_machine[1] = hold[2]["user"]
                remote_machine[2] = hold[2]["pass"]
                remote_machine[3] = hold[2]["path"]
        except:
            print "The config file is not arranged properly"
            exit(1)

    vms = VmManager(vm_list, backup_path)
    vms.stop_all_machines()
    sleep(10)  # prevent unreg cloning
    vms.clone_all_machines()
    sleep(10)  # wait for all stuff to finish job
    vms.start_all_machines()

    # Untoggle these lines if you want to replicate the backup locally to another path
    # for machine in vm_list:
    #    backup_machine_locally("", backup_path, machine[1])

    os.chdir(backup_path)
    files = [f for f in os.listdir(".")]

    for f in files:
        if deter_file_dates(f):
            print("Removing " + f)
            rmtree(f)

    f = FtpManager(remote_machine[0], remote_machine[1], remote_machine[2], remote_machine[3])
    f.connect()
    f.upload(backup_path)


