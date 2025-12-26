
import random
import string


starting_sn = 1000

def gen_sn():
    global starting_sn
    sn = starting_sn
    starting_sn += 1
    return sn
    
def gen_string(length):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

class Endpoint:
    def __init__(self, hardware_type:str):
        # Attributes
        if hardware_type == "EP1" or hardware_type == "EP2":
            self.battery_threshold = 2500
        elif hardware_type == "Canary_A":
            self.battery_threshold = 3600
        else:
            raise ValueError("Unknown hardware type")
        
        self.battery = 0  # default battery level
        self.backlog = 0  # default backlog
        self.version = 0  # default version
        self.hardware_type = hardware_type
        self.serial_number = hardware_type.upper() + "_" + str(gen_sn())

    # Setters and Getters
    def set_battery(self, battery_level):
        self.battery = battery_level
    def get_battery(self):
        return self.battery
    
    def set_backlog(self, backlog):
        self.backlog = backlog
    def get_backlog(self):
        return self.backlog
    
    def set_version(self, version):
        self.version = version
    def get_version(self):
        return self.version
    
    def get_serial_number(self):
        return self.serial_number
    def get_hardware_type(self):    
        return self.hardware_type
    # Constraints checks
    
    def check_threshold(self):
        return self.battery >= self.battery_threshold

    def check_backlog(self):
        return self.backlog == 0
    
        # Logic methods
    def update_version(self, new_version):
        if self.check_backlog() and self.check_threshold():
            self.version = new_version
            return True
        else:
            return False
        
class Node:
    def __init__(self, hardware_type:str, version:int=0):

        self.hardware_type = hardware_type  # type: str
        self.uuid = hardware_type.upper()+ "_" + gen_string(8)
        self.ota_channel = "OTA_" + self.uuid
        self.version = version
        self.endpoints = [Endpoint("EP1"),Endpoint("EP2"),Endpoint("Canary_A")]  # List of endpoint objects

    # Setters and Getters
    def set_version(self, version):
        self.version = version
    def get_version(self):
        return self.version
    def get_ota_channel(self):
        return self.ota_channel
    def get_endpoints(self):
        for ep in self.endpoints:
            print(f"Endpoint Serial Number: {ep.get_serial_number()}")
            