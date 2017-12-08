import os

class VmManager:
    def __init__(self, machines_list):
        self.machine_list = machines_list

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

    def stop_machine(self, machine_name):
        try:
            ret = os.system("vboxmanage controlvm \"" + machine_name + "\" poweroff")
        except:
            # todo log exception if something went wrong
            pass

    def clone_machine(self, machine_name, new_name):
        try:
            os.system("vboxmanage clonevm " + machine_name + " --name " + new_name + " --register")
        except:
            # todo log exception if something went wrong
            pass
