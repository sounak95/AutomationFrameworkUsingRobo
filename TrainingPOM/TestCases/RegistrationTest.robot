*** Settings ***
Resource  ../GenericConfig/ImportFile.robot
Test Setup     Open my browser    ${url}    ${browser} 
Test Teardown    Close All Browsers

#robot -d Results TestCases
Documentation    Registering in the application
...    
*** Variables ***
# ${Browser}    firefox
# ${SuiteUrl}    http://newtours.demoaut.com



*** Test Cases ***
Registration Test
    [Documentation]    Test case to perform the registration process
    
    Click Register Link
    Enter FirstName    Abir
    Enter LastName    Roy
    Enter Phone    9876543212
    Enter Email    abir31@gmail.com
    Enter Address1    22 Camac Street
    Enter Address2    13 Lane
    Enter City    Kolkata
    Enter State    West Bengal
    Enter Postcode    700067
    Select Country    INDIA
    Enter User    abir31
    Enter pass       test123
    Enter Confirmed password    test123
    Click Submit
    Wait Until Page Contains    Thank you for registering.    30
    sleep    2
    
        
    
    