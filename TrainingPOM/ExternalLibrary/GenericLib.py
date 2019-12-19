import os
from robot.libraries.BuiltIn import BuiltIn

import collections
from robot.api import logger

import pandas as pd
import numpy as np
import math


class GenericLib(object):


    ROBOT_LIBRARY_VERSION = 3.0



    def execute_keyword_with_multiple_data(self, templateName, dataSet, datarow="None", sheetName="Sheet1",
                                               continue_on_failure='true', show_report='false',
                                               show_list_of_column_names=[]):
        """| Usage |
         This keyword is used to run template with multiple data.

         Data to template is passed either from an external file or directly using data dictionary or list of data dictionary from testcase to this keyword.

         It supports different format for an external file like: csv, txt, xlsx, xls.

         To run particular row data : Add 'rowid' column in dataSet file that contains ID(1,2,3..) for row data.

         By default, this keyword will take all row data present in the given 'dataSet' file.To run particular row, set 'datarow' parameter.

         Note: Please avoid using "." in column names as this keyword will ignore the text that comes after "." in column names

         | Arguments |

         'templateName' : Keyword name.

         'dataSet'      : Data file or data dictionary or list of data dictionary.

         'datarow'[Optional]      :

                                 1. To pass single row data : datarow=RowID   [Example: datarow=2]

                                 2. To pass multiple random row data : datarow=RowID1,RowID2..   [Example: datarow=2,6,8,3]

                                 3. To pass row present in some range : datarow=RowID1-RowID4   [Example: datarow=10-15]

         'sheetName'[Optional] : If 'dataSet' is an xlsx or xls file with different sheet name then pass data sheet name.

         'continue_on_failure' [Optional] : If keyword fails for some row and you do not want to continue with remaining rows then set continue_on_failure to false.
                                            By default, it is set to 'true'

         'show_report' [Optional] : By setting this argument to 'true', it allows user to see the Execution Report for 'rowid' and 'status' columns in html format on the log.html file.
                                    By default, it is set to 'false'. Usage is shown in example 7 and 8.

         'show_list_of_column_names' [Optional] : This option allows users to pass the columns names from dataSet, which are to be added in the Execution Report in the form of a list.
                                                  Once passed as a list, the column names are shown after 'rowid' and 'status' columns in the Execution Report.
                                                  Usage is shown in example 8.
        
         * External file data format :

         1. CSV file : data are separated by comma. First row has parameter name stored like 'ID','Branch'...etc and from second row start storing rows of data for respective parameter.

         2. Text file : data can be separated by comma,semicolon or tab.

          First line should have 'sep' parameter like sep=; or sep=, or sep=tab. Second line has parameter name stored like 'ID','Branch'...etc and from third line start storing data separated by 'sep' parameter for respective parameter.

         3. Excel file(xls or xlsx): First row has parameter name.Start storing data from second row.

         Note: In Order to skip any error related to Column not found in the data sheet and continue the execution, declare a variable
                named skip_error in a python file containing the substring of the error string that's common to all the fields
                 and import that file in the "Variables" section of the test case.
                e.g
                skip_error = "Dictionary variable '&{Alldata}' has no key"
                    in GenericConfig.py file

        |Example|

         1. To parse all row data present in external file :
         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | sheetName=${sheetname} |

         2. To parse single row data present in external file, pass particular row id to 'datarow' parameter:
         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | datarow=23| sheetName=${sheetname} |

         3. To parse multiple row data present in external file, pass all row id to 'datarow' parameter separated by ','
         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | datarow=23,25,78| sheetName=${sheetname} |

         4. To parse range of row data present in external file, pass starting row id and end row id to 'datarow' parameter separated by '-'
         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | datarow=20-25| sheetName=${sheetname} |

         5. To parse range of row data present in external file and do not continue if any datarow fails.
         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | datarow=20-25| sheetName=${sheetname} | continue_on_failure=false |

         6. To parse dictionary data :

         *** Variable ***
         |&{dataDict}| name=xyz | ID=234 |

         *** TestCases ***
         |Mx Execute Template With Multiple Data| Template_name | ${dataDict} |

         7. To show Execution Report in log file.
         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | sheetName=${sheetname} | show_report=true |

         8. To Show Execution Report with column names and column data in log file.

         *** Variable ***
         |@{ColumnDict}| URL | Username | Password |

         *** TestCases ***
         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | sheetName=${sheetname} | show_report=true | show_list_of_column_names=@{ColumnDict} |
        """
        try:
            template_parameters = {}
            table_header = """*HTML*
                           <div><div><table>
                           <caption><b>Execution Report</b></caption>
                           <tr><td style="background:#5CBFDE;text-align:center">rowid</td>
                           <td style="background:#5CBFDE;text-align:center">Status</td>
                           """
            for item in show_list_of_column_names:
                table_header = table_header+'<td style="background:#5CBFDE;text-align:center">' +item +'</td>'
            table_header = table_header + '</tr>'
            table_rows = ''
            error_found = ""
            global template_return_values
            continue_on_failure = str(continue_on_failure)
            data_type = type(dataSet)
            if data_type is collections.OrderedDict or data_type is dict or 'robot.utils.dotdict.DotDict' in str(data_type):
                try:
                    return_values = BuiltIn().run_keyword(templateName, dataSet)
                    status = "PASS"
                except Exception as e:
                    error_found = "{}\n".format(e)
            else:
                if data_type is list:
                    template_parameters = dataSet
                    status = "PASS"
                else:
                    if not os.path.isfile(dataSet):
                        raise AssertionError("Invalid Input Error ! \nFile {} does not exist.".format(dataSet))
                    else:
                        template_parameters, status = self._get_all_data_from_file(dataSet, str(datarow), sheetName) #------- Get all data from dataSet file and store in template_parameters
                return_values = collections.OrderedDict()
                r = 1
                for parameter in template_parameters:
                    flag_exc=0
                    if datarow == "None":
                        rowId = r
                        r = r+1

                    else:
                        rowId = int(parameter['rowid'])
                    try:
                        if continue_on_failure.lower() == 'false':
                            status1, value = BuiltIn().run_keyword_and_ignore_error(templateName, parameter)
                            if status1 == "FAIL":
                                raise AssertionError("FAIL")
                        else:
                            status1, value = BuiltIn().run_keyword_and_ignore_error(templateName, parameter)
                            if status1 == "FAIL":
                                logger.fail("failed")
                    except Exception as err:
                        flag_exc = 1
                        return_values[str(rowId)] = "Fails"
                        error_found = "{}\n".format(err)
                        table_rows = table_rows + """
                                     <tr><td style="background:red;text-align:center">""" + str(rowId) + '</td>'\
                                     '<td style="background-color:red;text-align:center">' + str(status1) + '</td>'

                        for item in show_list_of_column_names:
                            if item in parameter:
                                value1 = str(parameter[item])
                                table_rows = table_rows + """<td style="background-color:red;text-align:center">""" + str(value1) + '</td>'
                            else:
                                value1 = "DATA NOT FOUND!!"
                                table_rows = table_rows + """<td style="background-color:orange;text-align:center">""" + str(value1) + '</td>'

                        table_rows = table_rows + '</tr>'
                        if value:
                            return_values[str(rowId)] = value
                        if continue_on_failure.lower() == 'false':
                            break
                    if flag_exc == 0:
                        table_rows = table_rows + """<tr><td style="background-color:green;text-align:center">""" + str(rowId) + '</td>'\
                                         '<td style="background-color:green;text-align:center">' + str(status1) + '</td>'


                        for item in show_list_of_column_names:
                            if item in parameter:
                                value1 = str(parameter[item])

                                table_rows = table_rows + """<td style="background-color:green;text-align:center">""" + str(value1) + '</td>'
                            else:
                                value1 = "DATA NOT FOUND!!"
                                table_rows = table_rows + """<td style="background-color:orange;text-align:center">""" + str(value1) + '</td>'
                        table_rows = table_rows + '</tr>'
                        if value:
                            return_values[str(rowId)] = value
            del template_parameters
            template_return_values = ""
            if type(return_values) is collections.OrderedDict:
                if len(list(return_values.values())) == 1:
                    template_return_values = list(return_values.values())[0]
                else:
                    template_return_values = return_values
            elif type(return_values) is str or type(return_values) is str:
                template_return_values = return_values
            else:
                template_return_values = None
            if status != "PASS" and error_found == "":
                raise AssertionError(status)
            elif status == "PASS" and error_found != "":
                raise AssertionError("Mx Execute Template With Multiple Data keyword failed for some data")
            elif status != "PASS" and error_found != "":
                raise AssertionError(
                    "Error: \n{}\n Mx Execute Template With Multiple Data keyword failed for some data".format(status))
            else:
                logger.info("Mx Execute Template With Multiple Data keyword passed for all the data")
        except Exception as err:
            raise AssertionError(err)
        finally:
            if show_report.lower() == 'true':
                print(table_header+table_rows)

    def return_value_from_keyword(self):
        """|Usage|
         Used to return value from 'Mx Execute Template With Multiple Data' keyword if the passed template or keyword is returning any value

        |Example|
         1. If 'Mx Execute Template With Multiple Data' keyword is running for more than one row data present in dataset file then dictionary will be return with 'rowid' as the dictionary key.

         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | datarow=120-124 | sheetName=${sheetname} |
         |${v} | Mx Return Value From Template |

         2. If 'Mx Execute Template With Multiple Data' keyword is running for single row data present in dataset file or dictionary variable passed then this keyword will return single value

         |Mx Execute Template With Multiple Data| Template_name | ${XLSXexcel_file} | datarow=120 | sheetName=${sheetname} |
         |${v} | Mx Return Value From Template |


        """
        try:
            return template_return_values
        except:
            raise AssertionError("No Value returned from 'Mx Execute Template With Multiple Data' keyword !!!")

    def _get_all_data_from_file(self, filename, datarow="None", sheetName='Sheet1'):
        """Usage: To read the file and return all row data in dictionary and then store each row dictionary data inside a list and returns list of dictionary.
         Type of file supported : csv , txt, xls, xlsx type of files.
        """
        if datarow != "None":
            rowNumbers = []  # get row numbers to fetch row data from file.
            if ',' in datarow:
                rowNumbers = datarow.split(",")
            elif '-' in datarow:
                rowRange = datarow.split("-")
                startRow = int(rowRange[0])
                EndRow = int(rowRange[1])
                for i in range(startRow, EndRow + 1):
                    rowNumbers.append(str(i))
            else:
                rowNumbers.append(datarow)
        name, fileFormat = os.path.splitext(filename)  # ----- Get file format
        fileFormat = fileFormat.replace(".", "")
        AllData = []  # ------- Store file data in AllData list
        RowNotFound = []
        if fileFormat in ['xls', 'xlsx', 'csv']:
            if fileFormat == 'csv':
                df_csv = pd.read_csv(filename, dtype=str, na_filter=False)
            elif fileFormat in ['xls', 'xlsx']:
                df_csv = pd.read_excel(filename, sheetName, dtype=str, na_filter=False)
            if datarow != "None":
                for item in rowNumbers:
                    if not np.any(df_csv['rowid'].values == str(item)):
                        RowNotFound.append(item)
                list_rows = df_csv[df_csv['rowid'].isin(rowNumbers)].values
            else:
                list_rows = df_csv.values
            # keyparam = df_csv.columns.values
            # ----------- uncomment above step to avoid splitting col names by "."
            keyparam = []
            for item in df_csv.columns.values:
                if ("$.." in str(item)):
                    keyparam.append(str(item))
                else:
                    keyparam.append(str(item).split('.')[0])
            # commenting for future reference
            # keyparam = df_csv.columns.str.split('.').str[0]
            AllData = []
            for r, row in enumerate(list_rows):
                fileRowData = collections.OrderedDict()
                for c, col in enumerate(row):
                    if isinstance(col, str):
                        val = str(col)
                    elif isinstance(col, float):
                        if math.isnan(col):
                            val = ""
                        elif col == int(col):
                            val = str(int(col))
                        else:
                            val = str(col)
                    elif isinstance(col, bool):
                        val = str(bool(col))
                    elif isinstance(col, int):
                        val = str(int(col))
                    else:
                        val = str(col)
                    if "${" in str(val):
                        try:
                            val = self._get_global_parameter(val)
                        except:
                            pass
                    fileRowData[keyparam[c]] = val.strip()
                AllData.append(fileRowData)
                del fileRowData

        elif fileFormat == 'txt':
            with open(filename, 'r') as fileobj:  # ----- Open ,read and close the file
                fileData = fileobj.readlines()
            if fileData[0].split('=')[
                0] != 'sep':  # ----check file separator (, or ; or tab. If file separator is tab then split by \t
                raise AssertionError("No separator is present in the given data source text file !!!")
            else:
                fileSeparator = (fileData[0].split('=')[-1]).replace("\n", "")
                if fileSeparator == 'tab':
                    keyparam = (fileData[1].replace("\n", "")).split('\t')
                else:
                    keyparam = (fileData[1].replace("\n", "")).split(fileSeparator)
                    # --------- Get all file row data, split it by file separator and then store each row data as a value and parameter-name as a key of row dictionary
                for item in range(2, len(fileData)):
                    fileRowData = collections.OrderedDict()
                    if fileSeparator == 'tab':
                        dataList = (fileData[item].replace("\n", "")).split('\t')
                    else:
                        dataList = (fileData[item].replace("\n", "")).split(fileSeparator)
                    for data in range(0, len(dataList)):
                        if 'rowid' in keyparam[data].lower():
                            keyparam[data] = 'rowid'
                        if "${" in str(dataList[data]):
                            try:
                                dataList[data] = self._get_global_parameter(str(dataList[data]))
                            except:
                                pass
                        fileRowData[keyparam[data]] = dataList[data]
                    AllData.append(fileRowData)
                    del fileRowData
                del fileData
        if len(RowNotFound) == 0:
            return AllData, "PASS"
        else:
            DatafileError = ""
            if RowNotFound != []:
                DatafileError = "Row ID: "
                for i in range(len(RowNotFound)):
                    if i == len(RowNotFound) - 1:
                        DatafileError += RowNotFound[i] + " not found in data file: " + filename
                    else:
                        DatafileError += RowNotFound[i] + ","
            if DatafileError != "":
                return AllData, DatafileError
            else:
                return AllData, "PASS"

    def _get_global_parameter(self, value):
        if "${" in value:
            value = value.replace("${", "<<").replace("}", ">>")
        if "<<" in value:
            paramCount = value.count('<<')
            if paramCount >= 1:
                varlist = []
                varValue = {}
                start = [pos for pos, char in enumerate(value) if char == "<"]
                end = [pos for pos, char in enumerate(value) if char == ">"]
                start = [start[i] for i in range(0, len(start)) if i % 2 != 0]
                end = [end[i] for i in range(0, len(end)) if i % 2 != 0]
                [varlist.append(value[start[i] + 1:end[i] - 1]) for i in range(paramCount)]
                for l in varlist:
                    varValue[l] = BuiltIn().get_variable_value("${}".format(l))
                for k in list(varValue.keys()):
                    if varValue[k] != None:
                        value = value.replace("<<" + k + ">>", varValue[k])
                value = value.replace("<<", "${").replace(">>", "}")
        return value


