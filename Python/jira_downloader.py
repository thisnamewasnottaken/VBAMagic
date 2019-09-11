'''
Script to authenticate against JIRA and draw down a paginated JSON file containing all records of the provided project code and server.
References inlcude:
# https://blog.deiser.com/en/seven-ways-to-export-jira-issues
# https://developer.atlassian.com/server/jira/platform/rest-apis/
# https://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python#17306347
# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
'''
import sys
import getpass
import requests
import pandas as pd
import json
import unittest
import pprint
 
def wait_for_enter():
    input("Press Enter to continue: ")
 
def check_Config(context):
    print("The following context is applied to this script:")
    print("The project server is " + context["jira_server"])
    print("The project code is: " + context["jira_project"])
    return context

def get_Max_Parameters(context):
    """Get the JIRA server API config with a zero results JQL query
    
    Args:
        context: Dictionary of configuration values.

    Returns:
        context: New version of context
    """

    headers = { 'Content-Type' : 'application/json'}
    parameters = {
            #'project' : context["jira_project"],
            'jql': context["jql"],
            'maxResults' : context["maxResults"]
            }
    try:
        myResponse = requests.get(
                        context["jira_server"], 
                        headers=headers, 
                        params=parameters)
        data = myResponse.json()
        return int(data["total"])
    except:
        return ValueError("Check connection input details.")

def download_jira_data(context):
    '''Downloads the issue list from JIRA
    Args:
        context: configuration context

    Returns:
        dict. a json dictionary with issues.
    
    '''

    #try:
        #with csv.writer(open("test.csv", "wb+")) as f:
            # Write CSV Header, If you dont need that, remove this line
        #    f.writerow(["pk", "model", "codename", "name", "content_type"])
    data = {}
    for i in range(int(context["startAt"]),int(context["Total"]),int(context["maxResults"])):

        headers = { 'Content-Type' : 'application/json',
                    "Accept-Encoding": "gzip, deflate"}
        parameters = {
                    'jql': context["jql"],
                    'startAt': i,
                    'maxResults' : int(context["maxResults"]),
                    'fields' : "key,status,project,priority,issuetype,created,statuscategory"
                    }
        print(          context["jira_server"], 
                        headers, 
                        parameters)
        myResponse = requests.get(
                        context["jira_server"], 
                        headers=headers, 
                        params=parameters)

        # Load the JSON data into a variable for processing. 
        rawtemp = json.loads(myResponse.content)["issues"]

        for rawtempitems in rawtemp:
            varfieldtemp = {}
            for j in parameters["fields"].split(","):
                try:
                    varfieldtemp[j] = i["fields"][j]["'name'"] 
                except:
                    varfieldtemp[j] = None
            data[rawtempitems["key"]]= varfieldtemp
    pass
        # json.loads(myResponse.content)["issues"][0]["key"]
        
        # json.loads(myResponse.content)["issues"][0]["fields"]

        #   for issues in data:
        #       f.writerow([issues["key"]])
    return data

        
    #except:
    #    print("hey")
    #    return ValueError("Check connection input details.")


    # For successful API call, response code will be 200 (OK)
    # if(myResponse.ok):
    #     myResponse.json()
    #     # Loading the response data into a dict variable
    #     # json.loads takes in only binary or string variables so using content to fetch binary content
    #     # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
                    
    #     jData = json.loads(myResponse.content)
    #     print(json.dumps(jData, indent=4, sort_keys=True))

    #     print("The response contains {0} properties".format(len(jData)))
    #     print("\n")

    # else:
    # # If response code is not ok (200), print the resulting http error code with description
    #     myResponse.raise_for_status()

    #wait_for_enter() 
        
def main():
    check_Config(context)
    context["Total"] = get_Max_Parameters(context)
    download_jira_data(context)


if __name__ == "__main__":
    context = {
        "username": getpass.getuser(),
        "password": getpass.getpass,
        "jira_server": 'https://jira.atlassian.com/rest/api/latest/search?',
        "jira_project": 'JSWCLOUD',
        "jql": 'project = JSWCLOUD AND resolution = Unresolved ORDER BY priority DESC, updated DESC',
        "jira_test_issue":'JSWCLOUD-17275',
        "testurl":'https://jira.atlassian.com/rest/api/latest/search?project=JSWCLOUD&expand=names,renderedFields',
        "maxResults": "3",
        "Total":"0",
        "startAt":"0"
        }
    main()

    print("Done.")