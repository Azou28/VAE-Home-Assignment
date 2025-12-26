from IoT_Environment import Env

def api_init_environment():
    global env
    env = Env()
    
def api_get_all_nodes() -> list:
    nodes_list = []
    for node in env.nodes:
        nodes_list.append(node.get_uuid())
    return nodes_list

def api_get_node_by_uuid(uuid: str) -> dict:
    node = env.get_node(uuid)
    if node is None:
        return {}
    return node

def api_get_endpoint_by_serial(serial_number: str) -> dict:
    ep = env.get_ep_by_serial(serial_number)
    if ep is None:
        return {}
    return ep

def api_post_version_to_ota_channel(ota_channel: str, version_artifact: str) -> int:
    # Adds new version to channel
    return env.post_version_to_ota_channel(ota_channel, version_artifact)

def api_clear_ota_channel(ota_channel: str) -> int:
    # Clear an artifact from the OTA channel
    return env.clear_ota_channel(ota_channel)

def api_set_node_version(uuid: str, version: int):
    for node in env.nodes:
        if node.uuid == uuid:
            node.version = version
            return 200
    return 400

def api_reset_environment():
    env.reset_env()