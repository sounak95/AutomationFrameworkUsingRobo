
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
    Execute Keyword With Multiple Data    Register User Test    ${Registration_data_file}    sheetName=Sheet1 
