# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class GithubOrganization(models.Model):
    _name = 'github.organization'
    _inherit = ['abstract.github.model']
    _order = 'name'

    # Columns Section
    name = fields.Char(
        string='Organization Name', required=True, readonly=True)

    billing_email = fields.Char(string='Billing Email', readonly=True)

    image = fields.Binary(string='Image', readonly=True)

    description = fields.Char(string='Description', readonly=True)

    email = fields.Char(string='Email', readonly=True)

    website_url = fields.Char(string='Website URL', readonly=True)

    location = fields.Char(string='Location', readonly=True)

    ignored_repository_names = fields.Text(
        string='Ignored Repositories', help="Set here repository names you"
        " you want to ignore. One repository per line. Exemple:\n"
        "odoo-community.org\n"
        "OpenUpgrade\n")

    member_ids = fields.Many2many(
        string='Members', comodel_name='res.partner',
        relation='github_organization_partner_rel', column1='organization_id',
        column2='partner_id', readonly=True)

    member_qty = fields.Integer(
        string='Members Quantity', compute='_compute_member_qty',
        store=True)

    repository_ids = fields.One2many(
        string='Repositories', comodel_name='github.repository',
        inverse_name='organization_id', readonly=True)

    repository_qty = fields.Integer(
        string='Repositories Quantity', compute='_compute_repository_qty',
        store=True)

    team_ids = fields.One2many(
        string='Teams', comodel_name='github.team',
        inverse_name='organization_id', readonly=True)

    team_qty = fields.Integer(
        string='Team Quantity', compute='_compute_team_qty',
        store=True)

    # Overloadable Section
    def github_type(self):
        return 'organization'

    def github_login_field(self):
        return 'login'

    @api.model
    def get_odoo_data_from_github(self, data):
        res = super(GithubOrganization, self).get_odoo_data_from_github(data)
        res.update({
            'name': data['name'],
            'description': data['description'],
            'location': data['location'],
            'website_url': data['blog'],
            'email': data['email'],
            'billing_email': data['billing_email'],
            'image': self.get_base64_image_from_github(data['avatar_url']),
        })
        return res

    @api.multi
    def full_update(self):
        self.button_sync_member()
        self.button_sync_repository()
        self.button_sync_team()

    # Compute Section
    @api.multi
    @api.depends('member_ids')
    def _compute_member_qty(self):
        # TODO FIXME, recompute is not called when a member is deleted (M2M)
        for organization in self:
            organization.member_qty =\
                len(organization.member_ids)

    @api.multi
    @api.depends('repository_ids.organization_id')
    def _compute_repository_qty(self):
        for organization in self:
            organization.repository_qty =\
                len(organization.repository_ids)

    @api.multi
    @api.depends('team_ids.organization_id')
    def _compute_team_qty(self):
        for organization in self:
            organization.team_qty =\
                len(organization.team_ids)

    # Action section
    @api.multi
    def button_sync_member(self):
        partner_obj = self.env['res.partner']
        for organization in self:
            member_ids = []
            for data in self.get_datalist_from_github(
                    'organization_members', [organization.github_login]):
                partner = partner_obj.get_from_id_or_create(data)
                member_ids.append(partner.id)
            organization.member_ids = member_ids

    @api.multi
    def button_sync_repository(self):
        repository_obj = self.env['github.repository']
        for organization in self:
            repository_ids = []
            ignored_list = organization.ignored_repository_names and\
                organization.ignored_repository_names.split("\n") or []
            for data in self.get_datalist_from_github(
                    'organization_repositories', [organization.github_login]):
                if data['name'] not in ignored_list:
                    repository = repository_obj.get_from_id_or_create(data)
                    repository_ids.append(repository.id)
            organization.repository_ids = repository_ids

    @api.multi
    def button_sync_team(self):
        team_obj = self.env['github.team']
        for organization in self:
            team_ids = []
            for data in self.get_datalist_from_github(
                    'organization_teams', [organization.github_login]):
                team = team_obj.get_from_id_or_create(data)
                team_ids.append(team.id)
            organization.team_ids = team_ids

#    organization_serie_ids = fields.One2many(
#        string='Organization Series',
#        comodel_name='github.organization.serie',
#        inverse_name='organization_id')