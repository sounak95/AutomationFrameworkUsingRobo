*** Settings ***
Resource  ../GenericConfig/ImportFile.robot
Test Setup     Open my browser    ${url}    ${browser} 
Test Teardown    Close All Browsers
*** Variables ***
# ${Browser}    firefox
# ${SuiteUrl}    http://newtours.demoaut.com
${user}    tutorial
${password}    tutorial


*** Test Cases ***
LoginTest
   
    LoginKeywords.Enter UserName    ${user}
    LoginKeywords.Enter Password    ${password}
    Click SignIn
    sleep    3
    Verify Successful login
    # Close All Browsers
