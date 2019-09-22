'''
Script to authenticate against JIRA and draw down a paginated JSON file containing all records of the provided project code and server.
References inlcude:
# https://blog.deiser.com/en/seven-ways-to-export-jira-issues
# https://developer.atlassian.com/server/jira/platform/rest-apis/
# https://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python#17306347
# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
'''
import getpass
import io
import json
import pprint
import sys
import unittest

import atlassian
import pandas as pd
import requests


def get_response_envelope(context):
    """Sends a zero results JQL query to the project server to see what the current and maximum parameters are.
    Assumes no authentication required, that's your problem.
    
    Args:
        context: dict, Configuration values for script.
            'jira_server':  Jira server, e.g. 'https://jira.atlassian.com'
            'jira_jql':     Jira jql query, e.g. project = JSWCLOUD AND resolution = Unresolved ORDER BY priority DESC, updated DESC'

    Returns:
        dict, 
            'total':        Number of issues in jql
            'startAt':      Current starting point
            'expand':       Current expand setting
            'maxResults'    API Max Results setting from server.
    """
    try:
        resp = atlassian.Jira(url=context["jira_server"]).jql(context["jira_jql"],limit=0)
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
    data.to_csv (context.get("csv_destination_file"), index = None, header=True)


def run(context):
    print("jira_downloader: Main run starting.")
    if context.get("jira_total_entries") is None:
        print("jira_downloader: Setting record limit as none was provided.")
        context["jira_total_entries"] = get_response_envelope(context)["total"]
    print("jira_downloader: Downloading data.")
    data = get_jira_data(context)
    print("jira_downloader: Exporting...")
    write_jira_csv_export(context, data)
    print("jira_downloader: Exporting...")


if __name__ == "__main__":
    run(context)                        #pylint: disable=undefined-variable 
    if context is None:                 #pylint: disable=undefined-variable
        raise NotImplementedError()
