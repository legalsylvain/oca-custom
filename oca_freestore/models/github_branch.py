# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api

from .tools import get_from_github, get_base64_image_from_url


class GithubRepository(models.Model):
    _name = 'github.repository'

    # Column Section
    organization_id = fields.Many2one(
        comodel_name='github.organization', string='Organization',
        required=True, select=True, readonly=True)

    name = fields.Char(
        string='Name', select=True, required=True, readonly=True)

    complete_name = fields.Char(
        string='Complete Name', select=True, required=True, readonly=True)

    description = fields.Char(string='Description', readonly=True)

    website = fields.Char(string='Website', readonly=True)

    github_url = fields.Char(string='Github URL', readonly=True)
        
    _sql_constraints = [
        (
            'complete_name_uniq', 'unique(complete_name)',
            "Two Projects with the same Complete Name ? I don't think so.")
    ]

    # Custom Section
    def github_2_odoo(self, data):
        return {
            'name': data['name'],
            'complete_name': data['full_name'],
            'github_url': data['url'],
            'website': data['homepage'],
            'description': data['description'],
        }

    # Custom Section
    @api.model
    def create_or_update_from_github(self, organization_id, data, full):
        """Create a new repository or update an existing one based on github
        datas. Return a repository."""
        repository = self.search([('complete_name', '=', data['full_name'])])

        if repository and not full:
            return repository

        # Get Full Datas from Github
        odoo_data = self.github_2_odoo(get_from_github(
                'https://api.github.com/repos/%s' % (data['full_name'])))
        odoo_data.update({'organization_id': organization_id})
        if not repository:
            repository = self.create(odoo_data)
        else:
            repository.write(odoo_data)

        return repository
        # TODO get branches https://api.github.com/repos/OCA/xxx/branches

