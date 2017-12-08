from ConfigManager import ConfigManager
from VmManager import VmManager
import os


def backup_machine_locally(from_path, to_path, machine_bkp_name):
    os.system("\cp " + from_path + "/" + machine_bkp_name + " " + to_path + "/" + machine_bkp_name)

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
        except:
            print "The config file is not arranged properly"
            exit(1)

    vms = VmManager(vm_list)
    vms.stop_all_machines()
    # todo add timer for stopping machines
    vms.clone_all_machines()

    for machine in vm_list:
        backup_machine_locally("", backup_path, machine[1])


