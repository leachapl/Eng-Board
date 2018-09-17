from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from . import jira
from .auth import rest_login_required

bp = Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/proddel/<string:proddel_key>/counts')
@rest_login_required
def proddel_counts(proddel_key):
    total_issues = jira.get_all_issues_for_proddel_ticket(g.user['auth'], proddel_key, 4)['total']
    closed_issues = jira.get_all_closed_issues_for_proddel_ticket(g.user['auth'], proddel_key, 4)['total']

    tkt = {
        'total_issues': total_issues,
        'closed_issues': closed_issues,
        'percent_complete': 0 if total_issues == 0 else int(round((closed_issues / total_issues) * 100)),
    }
    
    return jsonify(tkt)