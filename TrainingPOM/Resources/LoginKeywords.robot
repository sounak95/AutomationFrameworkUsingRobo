*** Settings ***
Resource   ../GenericConfig/ImportFileResource.robot



*** Keywords ***
Open my browser
    [Arguments]    ${SiteUrl}    ${Browser}
    Open Browser    ${SiteUrl}    ${Browser}
    Maximize Browser Window
    
Enter UserName
    [Arguments]    ${username}
    Input Text    ${txt_loginUserName}    ${username}
    
Enter Password
    [Arguments]    ${Password}
    Input Text    ${txt_loginPassword}    ${Password}
    
Click SignIn
    Click Button    ${btn_signIn}    
    
Verify Successful login
    Wait Until Page Contains    Passengers:     60s   
    Title Should Be    Find a Flight: Mercury Tours:    
    
     
     