import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import jira
from .auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    versions = jira.get_project_versions(g.user['auth'])
    unreleased_versions = filter(lambda version: version['archived'] == False and version['released'] == False, versions)
    return render_template('dashboard/index.html', versions=sorted(unreleased_versions, key = lambda version: version['name']))

@bp.route('/version/<int:versionid>')
@login_required
def version(versionid):
    proddel_tickets = []
    proddel_tickets_for_version = jira.get_proddel_tickets_for_version(g.user['auth'], str(versionid))
    for pd_ticket in proddel_tickets_for_version['issues']:
        status = ''
        if pd_ticket['fields']['status']['name'] == 'In Progress':
            status = 'inprogress'
        elif pd_ticket['fields']['status']['name'] == 'Closed':
            status = 'done'

        tkt = {
            'key': pd_ticket['key'],
            'summary': pd_ticket['fields']['summary'],
            'release': 'unknown',
            'status': status
        }
        proddel_tickets.append(tkt)
    return render_template('dashboard/version.html', proddel_tickets=proddel_tickets)
