'''
Script to authenticate against JIRA and draw down a paginated JSON file containing all records of the provided project code and server.
References:
# https://blog.deiser.com/en/seven-ways-to-export-jira-issues
# https://developer.atlassian.com/server/jira/platform/rest-apis/
# https://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python#17306347
# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
'''
import getpass
import json
import os
import unittest

import pandas

import jira_downloader


class Config_Related_Tests(unittest.TestCase):
    """Configuration related tests for the jira_downloader."""

    def setUp(self):
        """Fixture that sets the test variables to start with."""
        # Setting the default test context against the public jira project  

        with open('test_context.json') as json_context:
            self.context = json.load(json_context)
        self.data = pandas.read_json(path_or_buf=r'test_data.json' ,orient='table')


    def tearDown(self):
        """Fixture that deletes the files used by the test methods."""
        try:
            myfile = self.context.get("csv_destination_file")
            print("Trying to remove "+str(myfile))
            os.remove(myfile)
        except:
            pass
        try:
            self.context.clear
        except:
            pass


    def test_smoke_get_response_envelope(self):
        """Smoke test: Check if 'get_response_envelope' exist and runs"""
        jira_downloader.get_response_envelope(self.context)


    def test_smoke_get_jira_data(self):
        """Smoke test: Check if 'get_jira_data' exist and runs"""
        jira_downloader.get_jira_data(self.context)


    def test_smoke_write_jira_csv_export(self):
        """Smoke test: Check if 'write_jira_csv_export' exist and runs"""
        jira_downloader.write_jira_csv_export(self.context, self.data)


    def test_smoke_run(self):
        """Smoke test: Check if 'run' exist and runs"""
        jira_downloader.run(self.context)


class Functional_Tests(unittest.TestCase):
    """Functional tests for the jira_downloader."""

    def setUp(self):
        """Fixture that sets the test variables to start with."""
        # Setting the default test context against the public jira project  

        with open('test_context.json') as json_data:
            self.context = json.load(json_data)
        self.data = pandas.read_json(path_or_buf=r'D:\GitHub\VBAMagic\Python\test_data.json' ,orient='table')


    def tearDown(self):
        """Fixture that deletes the files used by the test methods."""
        try:
            myfile = self.context.get("csv_destination_file")
            print("Trying to remove "+str(myfile))
            os.remove(myfile)
        except:
            pass
        try:
            self.context.clear
        except:
            pass


    def test_smoke_get_response_envelope(self):
        """Smoke test: Check if 'get_response_envelope' exist and runs"""
        jira_downloader.get_response_envelope(self.context)

if __name__ == '__main__':
    unittest.main()
