import AuguryAPI as api


api.api_reset_environment()

def OTA_Happy_Flow_Test():
    node = api.api_get_node_by_uuid("AHN2_node-1000")
    print(f"Node data: {node}")

    rc = api.api_post_version_to_ota_channel("OTA_AHN2_node-1000", "AHN2_34.swu")
    print(f"Post OTA version to channel RC: {rc}")

    rc = api.api_apply_ota_updates("OTA_AHN2_node-1000")
    print(f"Apply OTA updates RC: {rc}")

    node = api.api_get_node_by_uuid("AHN2_node-1000")
    print(f"Node data after OTA update: {node}")

def test_endpoint_dfu_backlog():
    
    ep = api.api_get_endpoint_by_serial("EP1_ep-10000")
    print(f"Initial Endpoint data: {ep}")

    rc = api.api_set_endpoint_battery("EP1_ep-10000", 3000)
    rc = api.api_set_endpoint_backlog("EP1_ep-10000", 5)
    
    ep = api.api_get_endpoint_by_serial("EP1_ep-10000")
    print(f"Endpoint data: {ep}")
    
    rc = api.api_apply_dfu_updates_for_endpoint("EP1_ep-10000", "EP1_34.swu")
    for i in range(5, -1, -1):
        rc = api.api_set_endpoint_backlog("EP1_ep-10000", i)
        print(f"Set endpoint backlog to {i} RC: {rc}")
        rc = api.api_apply_dfu_updates_for_endpoint("EP1_ep-10000", "EP1_34.swu")
        print(f"Apply DFU updates for node RC: {rc}")
        if rc == 200:
            ep = api.api_get_endpoint_by_serial("EP1_ep-10000")
            print(f"Endpoint data after setting backlog to {i}: {ep}")

def Bad_Firmaware_OTA_Test():
    node = api.api_get_node_by_uuid("MOXA_node-1002")
    print(f"Node data: {node}")

    rc = api.api_post_version_to_ota_channel("OTA_MOXA_node-1002", "AHN2_34.swu")
    print(f"Post bad OTA version to channel RC: {rc}")

    rc = api.api_apply_ota_updates("OTA_MOXA_node-1002")
    print(f"Apply OTA updates RC: {rc}")

    node = api.api_get_node_by_uuid("MOXA_node-1002")
    print(f"Node data after bad OTA update attempt: {node}")    

if __name__ == "__main__":
    # OTA_Happy_Flow_Test()
    Bad_Firmaware_OTA_Test()
    # test_endpoint_dfu_backlog()
    # api.api_debug_print_environment()






