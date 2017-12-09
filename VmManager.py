import os
import time


class VmManager:

    def __init__(self, machines_list, base_folder):
        self.machine_list = machines_list
        self.base_folder = base_folder
        self.pattern = "%Y_%m_%d"

    def stop_all_machines(self):
        for machine in self.machine_list:
            if machine[0] != "":  # id
                self.stop_machine(machine[0])
            else:                 # name
                self.stop_machine(machine[1])

    def clone_all_machines(self):
        for machine in self.machine_list:
            if machine[0] != "":  # id
                self.clone_machine(machine[0])
            else:                 # name
                self.clone_machine(machine[1])

    def start_all_machines(self):
        for machine in self.machine_list:
            if machine[0] != "":  # id
                self.start_machine(machine[0])
            else:                 # name
                self.start_machine(machine[1])

    def stop_machine(self, machine_name):
        cmd = "vboxmanage controlvm \"" + machine_name + "\" poweroff"
        print cmd
        try:
            ret = os.system(cmd)
        except:
            # todo log exception if something went wrong
            pass

    def clone_machine(self, machine_name):
        today = time.strftime(self.pattern)
        cmd = "vboxmanage clonevm " + machine_name + " --name " + today + "_" + machine_name + " --basefolder " + self.base_folder
        print cmd
        try:
            os.system(cmd)
        except:
            # todo log exception if something went wrong
            pass

    def start_machine(self, machine_name):
        cmd = "vboxmanage startvm " + machine_name
        print cmd
        try:
            os.system(cmd)
        except:
            # todo log exception if something went wrong
            pass
