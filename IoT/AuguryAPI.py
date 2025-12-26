from IoT_Environment import Env

env = Env()


def api_get_node_by_uuid(uuid: str) -> dict:
    node = env.get_node(uuid)
    if node is None:
        print("Node not found")
        return {}
    else:
        print("Node found:")
        print(node)
    return node

def api_get_endpoint_by_serial(serial_number: str) -> dict:
    ep = env.get_ep_by_serial(serial_number)
    if ep is None:
        print("Endpoint not found")
        return {}
    else:
        print("Endpoint found:")
        print(ep)
    return ep

def api_post_version_to_ota_channel(ota_channel: str, version_artifact: str) -> int:
    # Adds new version to channel
    if env.post_version_to_ota_channel(ota_channel, version_artifact):
        return 200  # success   
    return 400 # fail

def api_clear_ota_channel(ota_channel: str, version_artifact: str) -> int:
    # Clear an artifact from the OTA channel
    return 200  # success
    return 400 # fail
