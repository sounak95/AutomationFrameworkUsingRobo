
*** Settings ***
Resource  ../GenericConfig/ImportFile.robot
#SET PYTHONPATH=D:\workspace1\TrainingPOM\ExternalLibrary
#robot -d Results TestCases\RegistrationDataDriven.robot
#pabot --processes 3 --outputdir PabotResults TestCases
#robot -d Results TestCases
Documentation    Registering in the application
...    
...    
*** Variables ***
# ${Browser}    firefox
# ${SuiteUrl}    http://newtours.demoaut.com



*** Test Cases ***

TC1
    Given Start Browser and Maximize
    And Click Register Link
    When Execute Keyword With Multiple Data    Register User    ${Registration_data_file}     datarow=1   sheetName=Sheet1 
    Then Close Session  
