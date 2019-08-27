'''
Script to authenticate against JIRA and draw down a paginated JSON file.
References:
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
 
def wait_for_enter():
    input("Press Enter to continue: ")
 
class CheckConfig(object):
    def run(self, context):
        print("The project server is {0}".format(context["jira_server"]))
        print(context["jira_server"])
        wait_for_enter()
 
class DownloadTest(object):
    def run(self, context):
        #jqlstring = str(context["jira_server"]) + 'rest/api/latest/issue/JSWCLOUD-17275
        #https://jira.atlassian.com/rest/api/latest/issue/JSWCLOUD-17275
        #r = requests.get('https://jira.atlassian.com/rest/api/latest/issue/JSWCLOUD-17275?expand=names,renderedFields') 

        # Replace with the correct URL
        url = "https://jira.atlassian.com/rest/api/latest/search?project=JSWCLOUD&expand=names,renderedFields"
        # It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
        # myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
        # myResponse = requests.get(url,verify=True)

        headers = { 'Content-Type' : 'application/json'
                        }

        parameters = {
                    'jql' : 'project IN (JSWCLOUD) AND statusCategory!=Done',
                    'startAt': 0,
                    'maxResults' : 50,
                    'fields' : "key,status,project,priority,issuetype,created,statuscategory"
                    }

        myResponse = requests.request("GET", url, headers=headers, params=parameters)



        print ("GET RESULT status_code " + str(myResponse.status_code))
        print ("GET RESULT ok " + str(myResponse.ok))
        print ("GET RESULT next " + str(myResponse.next))
        # For successful API call, response code will be 200 (OK)
        if(myResponse.ok):
            myResponse.json()
            # Loading the response data into a dict variable
            # json.loads takes in only binary or string variables so using content to fetch binary content
            # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
                        
            jData = json.loads(myResponse.content)
            print(json.dumps(jData, indent=4, sort_keys=True))

            print("The response contains {0} properties".format(len(jData)))
            print("\n")

        else:
        # If response code is not ok (200), print the resulting http error code with description
            myResponse.raise_for_status()













        wait_for_enter()

if __name__ == "__main__":
    context = {
        "username": getpass.getuser(),
        "jira_server": 'https://jira.atlassian.com',
        "jql": 'project = JSWCLOUD AND resolution = Unresolved ORDER BY priority DESC, updated DESC',
        "jira_test_issue":'JSWCLOUD-17275',
        "testurl":'https://jira.atlassian.com/rest/api/latest/search?project=JSWCLOUD&expand=names,renderedFields'
        
        }
    procedure = [
        CheckConfig(),
        DownloadTest()
    ]
    for step in procedure:
        step.run(context)
    print("Done.")

