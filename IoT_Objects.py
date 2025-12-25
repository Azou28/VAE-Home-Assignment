class Endpoint:
    def __init__(self, serial_number, battery, hardware_type, uuid, version):
        self.serial_number = serial_number
        self.battery = battery
        self.hardware_type = hardware_type
        self.uuid = uuid
        self.version = version

    def get_info(self):
        return {
            "serial_number": self.serial_number,
            "battery": self.battery,
            "hardware_type": self.hardware_type,
            "uuid": self.uuid,
            "version": self.version
        }
        
        
        
class Node:
    def __init__(self, ota_channel, uuid, version, endpoints):

        self.uuid = uuid
        self.ota_channel = ota_channel
        self.version = version
        self.endpoints = endpoints  # List of endpoint objects

    def get_info(self):
        return {
            "uuid": self.uuid,
            "ota_channel": self.ota_channel,
            "version": self.version,
            "endpoints": [endpoint.get_info() for endpoint in self.endpoints]
        }
        
        
        
    
    
