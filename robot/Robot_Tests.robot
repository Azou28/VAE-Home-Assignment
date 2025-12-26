*** Settings ***
Documentation     Robot tests for OTA behavior using AuguryAPI.py
Library           Collections
Library           ../IoT/AuguryAPI.py

Suite Setup       Reset Test Environment
Test Setup        Reset Test Environment

*** Variables ***
# UUIDs based on your current generator defaults and node creation order.
# If you change counters/start values, update these 3 lines.
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


*** Keywords ***
Reset Test Environment
    Api Reset Environment

Apply Ota Should Succeed
    [Arguments]    ${ota_channel}
    ${rc}=    Api Apply Ota Updates    ${ota_channel}
    Should Be Equal As Integers    ${rc}    200
