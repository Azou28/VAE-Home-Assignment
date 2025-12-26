
import random
import string


starting_sn = 1000
starting_string = 0xA0000

def gen_sn():
    global starting_sn
    sn = starting_sn
    starting_sn += 1
    return sn
    
def gen_string():
    global starting_string
    s = hex(starting_string)[2:].upper()
    starting_string += 1
    return s

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
    
    def check_hw_type(self, version_artifact:str):
        va_upper = version_artifact.upper()
        hw_type_upper = self.hardware_type.upper()
        return va_upper.startswith(hw_type_upper)
    
        # Logic methods
    def dfu_update(self, version_artifact:str):
        version_number = int(version_artifact.split("_")[-1][:-4])
        if version_number <= self.version: # no update needed
            return False
        if self.check_backlog() and self.check_threshold():
            if self.check_hw_type(version_artifact):
                self.version = version_number
                return True
        return False
        
class Node:
    def __init__(self, hardware_type:str, version:int=0):

        self.hardware_type = hardware_type  # type: str
        self.uuid = hardware_type.upper()+ "_" + gen_string()
        self.ota_channel = "OTA_" + self.uuid
        self.version = version
        self.endpoints = [Endpoint("EP1"),Endpoint("EP2"),Endpoint("Canary_A")]  # List of endpoint objects

        if hardware_type.upper() == "MOXA":
            self.api_address = "moxa_api.azure"
        else:
            self.api_address = "buildroot_api.azure"
        

    # Setters and Getters

    def get_version(self):
        return self.version
    def get_ota_channel(self) -> str:
        return self.ota_channel
    def get_endpoints(self) -> list:
        return self.endpoints
    def get_uuid(self) -> str:
        return self.uuid
    
    # Constraints check
    def check_ota_channel(self, ota_channel:str):
        if ota_channel == self.ota_channel:
            return True
        return False
    

    def check_hw_type(self, version_artifact:str):
        va_upper = version_artifact.upper()
        hw_type_upper = self.hardware_type.upper()
        return va_upper.startswith(hw_type_upper)


    # Logic methods
    def update_version(self, ota_channel:str, version_artifact:str):
        version_number = int(version_artifact.split("_")[-1][:-4])
        if version_number <= self.version: # no update needed
            return False
        if self.check_ota_channel(ota_channel) and self.check_hw_type(version_artifact):
            self.version = version_number
            return True
        return False