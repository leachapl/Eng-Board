import pytest

from engboard import jira

auth = 'c2Jlbm5ldHQ6dG1odXJ0dHBpYjE5Njg='

def test_check_login_with_good_auth():
    assert jira.check_login(auth) == True

def test_check_login_with_bad_username_and_password():
    bad_auth= 'sbennett:q232132'
    assert jira.check_login(bad_auth) == False

def test_get_project_versions_contains_versions():
    versions = jira.get_project_versions(auth)
    assert len(versions) != 0
    assert versions[0]['name'] == 'Transformation Server 2.1.0'

def test_get_proddel_tickets_for_version():
    version = 'AWS Migration'
    proddel_tickets = jira.get_proddel_tickets_for_version(auth, version)
    assert len(proddel_tickets['issues']) != 0
    assert proddel_tickets['issues'][0]['key'] == 'PRODDEL-664'

def test_get_all_issues_for_proddel_ticket():
    proddel_ticket = 'PRODDEL-149'
    depth = 4
    issues = jira.get_all_issues_for_proddel_ticket(auth, proddel_ticket, depth)
    assert len(issues['issues']) != 0
    assert issues['issues'][0]['key'] == 'SEARCH-489'

def test_get_all_closed_issues_for_proddel_ticket():
    proddel_ticket = 'PRODDEL-149'
    depth = 4
    issues = jira.get_all_closed_issues_for_proddel_ticket(auth, proddel_ticket, depth)
    assert len(issues['issues']) != 0
    assert issues['issues'][0]['key'] == 'SEARCH-489'
