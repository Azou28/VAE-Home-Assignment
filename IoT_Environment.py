from IoT_Objects import Node

class Env:
    def __init__(self):
        self.nodes = [Node("ahn2"),Node("cassia"),Node("moxa")]
        for node in self.nodes:
            print(f"Node UUID: {node.uuid}")
            for ep in node.endpoints:
                print(f"Endpoint Serial Number: {ep.get_serial_number()}")
                
    def reset_env(self):
        self.__init__()
        
    def get_node(self, uuid: str) -> dict:
        for node in self.nodes:
            if node.uuid == uuid:
                node_data = {
                    "uuid": node.get_uuid(),
                    "ota_channel": node.get_ota_channel(),
                    "version": node.get_version(),
                    "Endpoints": [node.endpoints]
                }
                return node_data
        return None
    
    def get_ep_by_serial(self, serial_number: str) -> dict:
        for node in self.nodes:
            for ep in node.endpoints:
                if ep.get_serial_number() == serial_number:
                    ep_data = {
                        "serial_number": ep.get_serial_number(),
                        "battery": ep.get_battery(),
                        "hardware_type": ep.get_hardware_type(),
                        "uuid": node.get_uuid(),
                        "version": ep.get_version()
                    }
                    return ep_data
        return None
    
    def post_version_to_ota_channel(self, ota_channel: str, version_artifact: str):
        for node in self.nodes:
            if node.update_version(ota_channel, version_artifact):
                return True
        return False
    
if __name__ == "__main__":
    env = Env()