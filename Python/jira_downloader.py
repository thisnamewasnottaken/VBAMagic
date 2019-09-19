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
from atlassian import Jira
import io

def wait_for_enter():
    input("Press Enter to continue: ")


def get_response_envelope(context):
    """Get the JIRA server API config with a zero results JQL query
    
    Args:
        context: dict, Configuration values for script.

    Returns:
        dict, 
            'total':        Number of issues in jql
            'startAt':      Current starting point
            'expand':       Current expand setting
            'maxResults'    API Max Results setting from server.

    """
    try:
        #resp = Jira(url=context["jira_server"],username= context["jira_username"], password= context["jira_server"]).jql(context["jira_jql"],fields=context["jira_fields"],limit=0)
        resp = Jira(url=context["jira_server"]).jql(context["jira_jql"],limit=0)
        resp = {k:v for (k,v) in resp.items() if k in ["total","startAt","expand","maxResults"]  }
        return resp
    except:
        print(Exception)


def get_jira_data(context):
    '''Downloads the issue list from JIRA
    Args:
        context: configuration context

    Returns:
        dict. a json dictionary with issues.
    
    '''
    data = pd.DataFrame()
    data = data.fillna(0)
    # Paginate through the data calls    
    tempmax = int(context["jira_maxResults"])
    totalrecords = int(context["jira_total_entries"])
    #jiraserver = context["jira_server"]

    data = pd.DataFrame()
    data = data.fillna(0)
    try:
        if tempmax > totalrecords:
            pager = totalrecords
        else:
            pager = tempmax

        for i in range(0,totalrecords,pager):
            if i == 0:    
                print("First block starting starting at "+str(i)+" in chunks of "+str(pager)+" , total "+str(totalrecords))
                url = str(context["jira_server"])+"/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery="+str(context["jira_jql"])+"&tempMax="+str(pager)+"&pager/start="+str(i)
                urlData = requests.get(url).content
                data = pd.read_csv(io.StringIO(urlData.decode('utf-8')),index_col=False)
            elif i <= (totalrecords-pager):
                print("Working on starting point "+str(i)+" in chunks of "+str(pager)+" , total "+str(totalrecords))
                url = str(context["jira_server"])+"/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery="+str(context["jira_jql"])+"&tempMax="+str(pager)+"&pager/start="+str(i)
                urlData = requests.get(url).content
                tdata = pd.read_csv(io.StringIO(urlData.decode('utf-8')),index_col=False)
                data = pd.concat([data, tdata],ignore_index=True,sort=False)
            elif i > (totalrecords-pager):
                print("Working on final block point "+str(i)+" in chunks of "+str(pager)+" , total "+str(totalrecords))
                pager = totalrecords-i
                url = str(context["jira_server"])+"/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery="+str(context["jira_jql"])+"&tempMax="+str(pager)+"&pager/start="+str(i)
                urlData = requests.get(url).content
                tdata = pd.read_csv(io.StringIO(urlData.decode('utf-8')),index_col=False)
                data = pd.concat([data, tdata],ignore_index=True,sort=False)
                print("Final block done")
    finally:
        print("Returning Data")
        return data


def write_jira_csv_export(context,data):
    try:
        export_csv = data.to_csv (r'C:\Users\maus\Downloads\test_export_dataframe.csv', index = None, header=True) 
    finally:
        print("write_jira_csv_export is complete")
    pass


def main():
    #get_response_envelope = get_response_envelope(context)
    context["jira_total_entries"] = get_response_envelope(context)["total"] #get_response_envelope["total"]
    data = get_jira_data(context)
    write_jira_csv_export(context, data)
    print("done")


if __name__ == "__main__":
    context = {
        "jira_username": getpass.getuser(),
        "jira_password": getpass.getpass,
        "jira_server": 'https://jira.atlassian.com',
        "jira_jql": 'project = JSWCLOUD AND resolution = Unresolved ORDER BY priority DESC, updated DESC',
        "jira_maxResults": "1000",
        "jira_total_entries":None,
        "jira_fields": ['key','status','project','priority','issuetype','created','statuscategory'],
        "csv_destination": None
        }
    main()

    print("Done.")