# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Github Connector',
    'version': '8.0.0.0.0',
    'category': 'Custom',
    'author': ['Sylvain LE GAL', 'Odoo Community Association (OCA)'],
    'summary': 'recover information from github repositories',
    'depends': [
        'base',
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'data/ir_cron.xml',
        'views/view_wizard_load_github_model.xml',
        'views/view_wizard_update_from_github.xml',
        'views/view_wizard_update_company_author.xml',
        'views/view_reporting.xml',
        'views/action.xml',
        'views/view_res_partner.xml',
        'views/view_github_organization.xml',
        'views/view_wizard_download_analyze_branch.xml',
        'views/view_github_repository.xml',
        'views/view_github_repository_branch.xml',
        'views/view_github_team.xml',
        'views/view_github_issue.xml',
        'views/view_github_comment.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'installable': True,
    'external_dependencies': {
        'python': ['git', 'markdown'],
    },
}
