

def api_get_endpoint_by_serial(serial_number: str) -> dict:
    return {
        "serial_number": serial_number,
        “battery”: “<battery>”
        "hardware_type": "<hardware_type>"
        “uuid”: “<uuid>” 
        “version”: “<version>”
    }

def api_get_node_by_uuid(uuid: str) -> dict:
	“uuid”: uuid
	“ota_channel”: “<ota_channel>”
	“version”: “<version”>
	“Endpoints”: <list of Endpoint object mapped to the node>

def api_post_version_to_ota_channel(ota_channel: str, version_artifact: str) -> int:
    # Adds new version to channel
    return 200  # success
    return 400 # fail

def api_clear_ota_channel(ota_channel: str, version_artifact: str) -> int:
    # Clear an artifact from the OTA channel
    return 200  # success
    return 400 # fail
