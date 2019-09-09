'''
Script to authenticate against JIRA and draw down a paginated JSON file containing all records of the provided project code and server.
References:
# https://blog.deiser.com/en/seven-ways-to-export-jira-issues
# https://developer.atlassian.com/server/jira/platform/rest-apis/
# https://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python#17306347
# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
'''
import unittest
import jira_downloader
 
class Config_Related_Tests(unittest.TestCase):
    """Configuration related tests for the jira_downloader."""

    def setUp(self):
        """Fixture that sets the test variables to start with."""
        # Setting the default test context against the public jira project  
        self.context = {
            "username": None,
            "password": None,
            "jira_server": 'https://jira.atlassian.com/rest/api/latest/search?',
            "jira_project": 'JSWCLOUD',
            "jql": 'project = JSWCLOUD AND resolution = Unresolved ORDER BY priority DESC, updated DESC',
            "jira_test_issue":'JSWCLOUD-17275',
            "testurl":'https://jira.atlassian.com/rest/api/latest/search?project=JSWCLOUD&expand=names,renderedFields',
            "Total":"0"
            }


    def tearDown(self):
        """Fixture that deletes the files used by the test methods."""
        try:
            self.context.clear
        except:
            pass

    def test_check_Config_runs(self):
        """Basic smoke test: does check_Config run."""
        jira_downloader.check_Config(self.context)

    def test_check_Config_values_pass(self):
        """Basic smoke test: sample confirming context values are passed through."""
        self.assertEqual(jira_downloader.check_Config(self.context)["jira_server"],'https://jira.atlassian.com/rest/api/latest/search?')

    def test_get_Max_Parameters_runs(self):
        """Basic smoke test: does MaxParameters run"""
        jira_downloader.get_Max_Parameters(self.context)

    def test_get_Max_Parameters_returns_Int(self):
        """Basic smoke test: does max_Parameters return the expected integer"""
        self.assertIsInstance(jira_downloader.get_Max_Parameters(self.context),int)





if __name__ == '__main__':
    unittest.main()