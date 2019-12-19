*** Settings ***
Resource  ../GenericConfig/ImportFileResource.robot 



*** Keywords ***
Click Register Link
    Click Link    ${link_Reg}
    
Enter FirstName
    [Arguments]    ${firstName}
    Input Text    ${txt_firstName}    ${firstName}
    
Enter LastName
    [Arguments]    ${lastName}
    Input Text    ${txt_lastName}    ${lastName}
    
Enter Phone
    [Arguments]    ${phone}
    ${result}    Run Keyword And Return Status    Page Should Contain Element    ${txt_phone}    
    Run Keyword If    '${result}'=='True'    Input Text    ${txt_phone}    ${phone}        
    ${val}=     Get Value    ${txt_phone}
    Log    ${val}  
    Should Be Equal As Strings    ${phone}      ${val}       
    
Enter Email
    [Arguments]    ${email}
    Input Text    ${txt_email}    ${email} 
    
Enter Address1
    [Arguments]    ${address1}
    Input Text    ${txt_add1}    ${address1} 
    
Enter Address2
    [Arguments]    ${address2}
    Input Text    ${txt_add2}    ${address2} 
    
Enter City
    [Arguments]    ${city}
    ${result}    Run Keyword And Return Status    Element Should Be Visible    ${txt_phone}    
    Run Keyword If    '${result}'=='True'    Input Text    ${txt_city}    ${city}       
    
    ${val}=    Get Element Attribute    ${txt_city}    name
    
Enter State
    [Arguments]    ${state}
    Input Text    ${txt_state}    ${state}
    
Enter Postcode
    [Arguments]    ${Postcode}
    Input Text    ${txt_postCode}    ${Postcode}
    
Select Country
    [Arguments]    ${country}
    Select From List By Label   ${drp_country}    ${country}  
    ${val}=    Get Selected List Label    ${drp_country}
    Log    ${val}
    ${val}=    Get List Items    ${drp_country} 
    log     ${val}     
    
Enter user
    [Arguments]    ${username}
    Input Text    ${txt_userName}    ${username}
    
Enter pass
    [Arguments]    ${password}
    Input Password    ${txt_password}    ${password}   
    
Enter Confirmed password
    [Arguments]    ${confpassword}
    Input Password    ${txt_conformedPassword}    ${confpassword}
    
Click Submit
    Click Button    ${btn_submit}   
 
Register User Test
    [Arguments]    ${Alldata1}
    Open browser    &{Alldata1}[URL]    &{Alldata1}[Browser]
    Click Register Link
	Enter FirstName    &{Alldata1}[FirstName]
	Enter LastName    &{Alldata1}[LastName]
	Enter Phone    &{Alldata1}[Phone]
	Enter Email    &{Alldata1}[Email]
	Enter Address1    &{Alldata1}[Address1]
	Enter Address2    &{Alldata1}[Address2]
	Enter City    &{Alldata1}[City]
	Enter State    &{Alldata1}[State]
	Enter Postcode    &{Alldata1}[PostCode]
	Select Country    &{Alldata1}[Country]
	Enter user    &{Alldata1}[Username]
	Enter pass    &{Alldata1}[Password]
	Enter Confirmed password    &{Alldata1}[Password]
	Click Submit
    Close All Browsers
    
Start Browser and Maximize
    Open browser    ${URL}    ${Browser}
    Maximize Browser Window
    
Register User
    [Arguments]    ${Alldata1}
    Enter FirstName    &{Alldata1}[FirstName]
	Enter LastName    &{Alldata1}[LastName]
	Enter Phone    &{Alldata1}[Phone]
	Enter Email    &{Alldata1}[Email]
	Enter Address1    &{Alldata1}[Address1]
	Enter Address2    &{Alldata1}[Address2]
	Enter City    &{Alldata1}[City]
	Enter State    &{Alldata1}[State]
	Enter Postcode    &{Alldata1}[PostCode]
	Select Country    &{Alldata1}[Country]
	Enter user    &{Alldata1}[Username]
	Enter pass    &{Alldata1}[Password]
	Enter Confirmed password    &{Alldata1}[Password]
	Click Submit

Close Session
    Close All Browsers
    
	
    

    
      
    
    

      
    
     
    
            