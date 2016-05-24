# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'OCA FreeStore',
    'version': '8.0.0.0.0',
    'category': 'Custom',
    'author': ['Akretion', 'GRAP', 'Odoo Community Association (OCA)'],
    'summary': 'recover information from github repositories',
    'depends': [
        'base',
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'views/view_res_partner.xml',
        'views/view_oca_license.xml',
        'views/view_oca_author.xml',
        'views/view_oca_python_lib.xml',
        'views/view_oca_bin_lib.xml',
        'views/view_oca_module.xml',
        'views/view_oca_module_version.xml',
        'views/view_github_organization.xml',
        'views/view_github_repository.xml',
        'views/view_github_repository_branch.xml',
        'views/view_github_team.xml',
        'views/view_git_commit.xml',
        'views/view_git_author.xml',
        'views/view_wizard_github_repository_branch.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/github_organization.xml',
        'demo/github_organization_serie.xml',
    ],
    'installable': True,
}
