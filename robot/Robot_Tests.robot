*** Settings ***
Documentation     Robot tests for OTA behavior using AuguryAPI.py
Library           Collections
Library           ../IoT/AuguryAPI.py

Suite Setup       Reset Test Environment
Test Setup        Reset Test Environment

*** Variables ***
# Node UUIDs
${UUID_AHN2}      AHN2_node-1000
${UUID_CASSIA}    CASSIA_node-1001
${UUID_MOXA}      MOXA_node-1002

# Versions
${START_VERSION}  33
${NEW_VERSION}    34

*** Test Cases ***
OTA Happy Flow - Update MOXA from 33 to 34
    [Documentation]    Upload valid MOXA firmware to MOXA OTA channel and apply update.
    ${node}=    Api Get Node By Uuid    ${UUID_MOXA}
    Should Not Be Empty    ${node}
    Should Be Equal As Integers    ${node["version"]}    ${START_VERSION}

    ${ota_channel}=    Set Variable    ${node["ota_channel"]}
    ${artifact}=       Set Variable    MOXA_${NEW_VERSION}.swu

    ${rc}=    Api Post Version To Ota Channel    ${ota_channel}    ${artifact}
    Should Be Equal As Integers    ${rc}    200

    # Retry pattern (simulates "device retries" style): keep applying until success
    Wait Until Keyword Succeeds    5x    0.2s    Apply Ota Should Succeed    ${ota_channel}

    ${node_after}=    Api Get Node By Uuid    ${UUID_MOXA}
    Should Be Equal As Integers    ${node_after["version"]}    ${NEW_VERSION}

Bad Firmware OTA - MOXA should NOT update from AHN2 artifact
    [Documentation]    Upload wrong firmware type to MOXA channel and verify version doesn't change.
    ${node}=    Api Get Node By Uuid    ${UUID_MOXA}
    Should Not Be Empty    ${node}
    Should Be Equal As Integers    ${node["version"]}    ${START_VERSION}

    ${ota_channel}=    Set Variable    ${node["ota_channel"]}
    ${bad_artifact}=   Set Variable    AHN2_${NEW_VERSION}.swu

    ${rc}=    Api Post Version To Ota Channel    ${ota_channel}    ${bad_artifact}
    Should Be Equal As Integers    ${rc}    200

    # Apply updates (should "succeed" at env level) but MOXA node must not change version
    ${apply_rc}=    Api Apply Ota Updates    ${ota_channel}
    Should Be Equal As Integers    ${apply_rc}    200

    ${node_after}=    Api Get Node By Uuid    ${UUID_MOXA}
    Should Be Equal As Integers    ${node_after["version"]}    ${START_VERSION}

Clear OTA Channel - Applying after clear should fail
    [Documentation]    Clear channel and ensure apply fails (no artifact).
    ${node}=    Api Get Node By Uuid    ${UUID_AHN2}
    Should Not Be Empty    ${node}

    ${ota_channel}=    Set Variable    ${node["ota_channel"]}
    ${artifact}=       Set Variable    AHN2_${NEW_VERSION}.swu

    ${rc}=    Api Post Version To Ota Channel    ${ota_channel}    ${artifact}
    Should Be Equal As Integers    ${rc}    200

    ${clear_rc}=    Api Clear Ota Channel    ${ota_channel}    ${artifact}
    Should Be Equal As Integers    ${clear_rc}    200

    ${apply_rc}=    Api Apply Ota Updates    ${ota_channel}
    Should Be Equal As Integers    ${apply_rc}    400

Endpoint DFU with Backlog and Battery Constraints
    [Documentation]    Endpoint must not update while backlog>0; must defer if battery<threshold.
    ${node}=    Api Get Node By Uuid    ${UUID_AHN2}
    Should Not Be Empty    ${node}

    # In this implementation the node endpoints are created in this fixed order: EP1, EP2, Canary_A
    ${ep1_serial}=    Set Variable    ${node["Endpoints"][0]}
    ${ep1}=    Api Get Endpoint By Serial    ${ep1_serial}
    Should Be Equal    ${ep1["hardware_type"]}    EP1

    # --- Backlog blocks update ---
    ${rc}=    Api Set Endpoint Backlog    ${ep1_serial}    5
    Should Be Equal As Integers    ${rc}    200
    ${rc}=    Api Set Endpoint Battery    ${ep1_serial}    3000
    Should Be Equal As Integers    ${rc}    200

    ${dfu_artifact}=    Set Variable    EP1_${NEW_VERSION}.swu
    ${rc}=    Api Post Version To Dfu Channel    EP1    ${dfu_artifact}
    Should Be Equal As Integers    ${rc}    200

    ${rc}=    Api Apply Dfu Updates For Node    ${UUID_AHN2}
    Should Be Equal As Integers    ${rc}    200
    ${ep1_after}=    Api Get Endpoint By Serial    ${ep1_serial}
    Should Be Equal As Integers    ${ep1_after["version"]}    0
    
    # Drain backlog -> update should happen
    ${rc}=    Api Set Endpoint Backlog    ${ep1_serial}    0
    Should Be Equal As Integers    ${rc}    200
    Wait Until Keyword Succeeds    5x    0.2s    DFU Should Update Endpoint    ${UUID_AHN2}    ${ep1_serial}    ${NEW_VERSION}

    # --- Battery blocks update ---
    Api Reset Environment
    ${node2}=    Api Get Node By Uuid    ${UUID_AHN2}
    ${ep1_serial2}=    Set Variable    ${node2["Endpoints"][0]}
    ${rc}=    Api Set Endpoint Backlog    ${ep1_serial2}    0
    Should Be Equal As Integers    ${rc}    200
    ${rc}=    Api Set Endpoint Battery    ${ep1_serial2}    2000
    Should Be Equal As Integers    ${rc}    200

    ${dfu_artifact}=    Set Variable    EP1_${NEW_VERSION}.swu
    ${rc}=    Api Post Version To Dfu Channel    EP1    ${dfu_artifact}
    Should Be Equal As Integers    ${rc}    200
    ${rc}=    Api Apply Dfu Updates For Node    ${UUID_AHN2}
    Should Be Equal As Integers    ${rc}    200
    ${ep1_low_batt}=    Api Get Endpoint By Serial    ${ep1_serial2}
    Should Be Equal As Integers    ${ep1_low_batt["version"]}    0

    # Raise battery above threshold -> update should happen
    ${rc}=    Api Set Endpoint Battery    ${ep1_serial2}    3000
    Should Be Equal As Integers    ${rc}    200
    Wait Until Keyword Succeeds    5x    0.2s    DFU Should Update Endpoint    ${UUID_AHN2}    ${ep1_serial2}    ${NEW_VERSION}


*** Keywords ***
Reset Test Environment
    Api Reset Environment

Apply Ota Should Succeed
    [Arguments]    ${ota_channel}
    ${rc}=    Api Apply Ota Updates    ${ota_channel}
    Should Be Equal As Integers    ${rc}    200

DFU Should Update Endpoint
    [Arguments]    ${node_uuid}    ${serial}    ${expected_version}
    ${rc}=    Api Apply Dfu Updates For Node    ${node_uuid}
    Should Be Equal As Integers    ${rc}    200
    ${ep}=    Api Get Endpoint By Serial    ${serial}
    Should Be Equal As Integers    ${ep["version"]}    ${expected_version}
