from IoT_Environment import Env

env = Env()

def api_debug_print_environment():
    env.debug_print()

def api_get_node_by_uuid(uuid: str) -> dict:
    node = env.get_node(uuid)
    if node is None:
        return {}
    return node

def api_get_endpoint_by_serial(serial_number: str) -> dict:
    ep = env.get_ep_dict_by_serial(serial_number)
    if ep is None:
        return {}
    return ep

def api_post_version_to_ota_channel(ota_channel: str, version_artifact: str) -> int:
    # Adds new version to channel
    return env.post_version_to_ota_channel(ota_channel, version_artifact)

def api_clear_ota_channel(ota_channel: str,version_artifact: str) -> int:
    # Clear an artifact from the OTA channel
    return env.clear_ota_channel(ota_channel)

def api_apply_ota_updates(ota_channel: str) -> int:
    return env.apply_ota_updates(ota_channel)


# ---- DFU (Endpoint firmware update) helpers ----

def api_apply_dfu_updates_for_endpoint(serial_number: str, version_artifact: str) -> int:
    return env.apply_dfu_updates_for_endpoint(serial_number,version_artifact)


def api_set_endpoint_battery(serial_number: str, battery: int) -> int:
    return env.set_ep_battery(serial_number, battery)


def api_set_endpoint_backlog(serial_number: str, backlog: int) -> int:
    return env.set_ep_backlog(serial_number, backlog)


def api_reset_environment():
    env.reset_env()