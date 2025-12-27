from IoT_Objects import Node,reset_counters
class Env:
    def __init__(self):
        self.nodes = [Node("ahn2"),Node("cassia"),Node("moxa")]
        # map ota_channel -> current artifact/version
        self.ota_channels = {node.get_ota_channel(): None for node in self.nodes}
                
    def reset_env(self):
        reset_counters()
        self.__init__()
        
    def debug_print(self):
        for node in self.nodes:
                    print(f"Node UUID: {node.uuid}")
                    for ep in node.endpoints:
                        print(f"Endpoint Serial Number: {ep.get_serial_number()}")
    
    def get_node(self, uuid: str) -> dict:
        for node in self.nodes:
            if node.uuid == uuid:
                ep_list = []
                for ep in node.endpoints:
                        ep_serial = ep.get_serial_number()
                        ep_list.append(ep_serial)
                node_data = {
                    "uuid": node.get_uuid(),
                    "ota_channel": node.get_ota_channel(),
                    "version": node.get_version(),
                    "Endpoints": ep_list
                }
                return node_data
        return None
    
    def get_ep_by_serial(self, serial_number: str):
        for node in self.nodes:
            for ep in node.endpoints:
                if ep.get_serial_number() == serial_number:
                    return ep
        return None
    
    def ep_to_dict(self, ep) -> dict:
        ep_data = {
            "serial_number": ep.get_serial_number(),
            "battery": ep.get_battery(),
            "backlog": ep.get_backlog(),
            "hardware_type": ep.get_hardware_type(),
            "uuid": ep.get_uuid(),
            "version": ep.get_version()
        }
        return ep_data
    
    def get_ep_dict_by_serial(self, serial_number: str):
        for node in self.nodes:
            for ep in node.endpoints:
                if ep.get_serial_number() == serial_number:
                    ep_to_dict = self.ep_to_dict(ep)
                    return ep_to_dict
        return None
    
    def set_ep_battery(self, serial_number: str, battery: int) -> int:
        ep = self.get_ep_by_serial(serial_number)
        if ep is None:
            return 400
        ep.set_battery(battery)
        return 200
    
    def set_ep_backlog(self, serial_number: str, backlog: int) -> int:
        ep = self.get_ep_by_serial(serial_number)
        if ep is None:
            return 400
        if ep.set_backlog(backlog):
            return 200
        return 201
    
    # ---- OTA helpers ----
    def post_version_to_ota_channel(self, ota_channel: str, version_artifact: str):
        if ota_channel in self.ota_channels:
            self.ota_channels[ota_channel] = version_artifact
            return 200  # Success
        return 400  # Fail
    
    def clear_ota_channel(self, ota_channel: str):
        if ota_channel in self.ota_channels:
            self.ota_channels[ota_channel] = None
            return 200  # Success
        return 400  # Fail

    def apply_ota_updates(self,ota_channel: str):
        if ota_channel not in self.ota_channels:
            return 400  # Fail
        version_artifact = self.ota_channels[ota_channel]
        if version_artifact is None:
            return 400  # Fail
        for node in self.nodes:
            node.update_version(ota_channel,version_artifact)
        return 200  # Success
        

    # ---- DFU helpers ----
    
    
    def apply_dfu_updates_for_endpoint(self, serial_number: str, version_artifact: str) -> int:
        ep = self.get_ep_by_serial(serial_number)
        if ep is None:
            return 400  # Fail
        if ep.dfu_update(version_artifact):
            return 200  # Success
        return 201  # No update applied
       
    
        