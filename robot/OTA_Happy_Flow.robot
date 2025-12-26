*** Settings ***
Library           IoT/AuguryAPI.py

*** Test Cases ***
OTA Happy Flow
    [Setup]    api init environment

    # 1) Init a Node with version 33 (either env defaults or a helper keyword)
    ${uuid}=    api get all nodes
    Set Node Version    ${uuid}    33

    ${node}=    api get node by uuid    ${uuid}
    Should Be Equal As Integers    ${node['version']}    33

    # 2) Upload a new version (34) to its OTA channel
    ${ota_channel}=    Set Variable    ${node['ota_channel']}
    ${artifact}=       Set Variable    moxa_34.swu
    ${status}=         Upload Version To Ota Channel    ${ota_channel}    ${artifact}
    Should Be Equal As Integers    ${status}    200

    # 3) After retries, confirm node version updated
    FOR    ${i}    IN RANGE    0    10
        Poll Node Ota Once    ${uuid}
        ${node}=    Get Node By Uuid    ${uuid}
        Exit For Loop If    ${node['version']} == 34
    END

    ${node}=    Get Node By Uuid    ${uuid}
    Should Be Equal As Integers    ${node['version']}    34
