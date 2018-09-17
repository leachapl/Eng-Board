import requests

def check_login(auth):
    # Checks login is able to return information from the PRODDEL board
    r = requests.get('https://issues.alfresco.com/jira/rest/api/2/project/PRODDEL', headers=request_headers(auth))
    return r.status_code == 200

def get_project_versions(auth):
    # fetches all versions for the PRODDEL board
    r = requests.get('https://issues.alfresco.com/jira/rest/api/2/project/PRODDEL/versions', headers=request_headers(auth))
    return r.json()

def get_proddel_tickets_for_version(auth, version):
    # fetches all PRODDEL tickets for a given named version
    params = {
        'jql': 'project=PRODDEL and fixVersion = "' + version + '"'
    }
    r = requests.get('https://issues.alfresco.com/jira/rest/api/2/search', headers=request_headers(auth), params=params)
    return r.json()

def get_all_issues_for_proddel_ticket(auth, proddel_ticket, depth):
    # fetches all descendent tickets for a given proddel ticket
    params = {
        'jql': 'issueFunction in linkedIssuesOfRecursiveLimited("issue = ' + proddel_ticket+ '",' + str(depth) + ') AND issuetype  in (story, epic)'
    }
    r = requests.get('https://issues.alfresco.com/jira/rest/api/2/search', headers=request_headers(auth), params=params)
    return r.json()

def get_all_closed_issues_for_proddel_ticket(auth, proddel_ticket, depth):
    # fetches all closed descendent tickets for a given proddel ticket
    params = {
        'jql': 'issueFunction in linkedIssuesOfRecursiveLimited("issue = ' + proddel_ticket+ '",' + str(depth) + ') AND issuetype  in (story, epic) AND status = "closed"'
    }
    r = requests.get('https://issues.alfresco.com/jira/rest/api/2/search', headers=request_headers(auth), params=params)
    return r.json()

def request_headers(auth):
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + auth
    }
