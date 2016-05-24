# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class GithubRepository(models.Model):
    _name = 'github.repository.branch'
    _inherit = ['abstract.github.model']

    _github_type = 'repository_branches'
    _github_login_field = False

    # Column Section
    name = fields.Char(
        string='Name', readonly=True, select=True)

    complete_name = fields.Char(
        string='Complete Name', store=True, compute='_compute_complete_name')

    repository_id = fields.Many2one(
        comodel_name='github.repository', string='Repository',
        required=True, select=True, readonly=True, ondelete='cascade')

    organization_id = fields.Many2one(
        comodel_name='github.organization', string='Organization',
        related='repository_id.organization_id', store=True, readonly=True)

    organization_serie_id = fields.Many2one(
        comodel_name='github.organization.serie', string='Organization Serie',
        compute='_compute_organization_serie_id', store=True)

    # Custom
    def create_or_update_from_name(self, repository_id, name):
        branch = self.search([
            ('name', '=', name), ('repository_id', '=', repository_id)])
        if not branch:
            branch = self.create({
                'name': name, 'repository_id': repository_id})
        return branch

    # Compute Section
    @api.multi
    @api.depends('name', 'repository_id.name')
    def _compute_complete_name(self):
        for branch in self:
            branch.complete_name =\
                branch.repository_id.name + '/' + branch.name

    # Compute Section
    @api.multi
    @api.depends('organization_id', 'name')
    def _compute_organization_serie_id(self):
        for branch in self:
            for serie in branch.organization_id.organization_serie_ids:
                if serie.name == branch.name:
                    branch.organization_serie_id = serie
