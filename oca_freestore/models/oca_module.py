# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api

class OcaModule(models.Model):
    _name = 'oca.module'

    # Column Section
    name = fields.Char(
        string='Name', select=True, required=True, readonly=True)

    module_version_ids = fields.One2many(
        comodel_name='oca.module.version', inverse_name='module_id',
        string='Versions')

    module_version_qty = fields.Integer(
        string='Module Version Quantity', compute='compute_module_version_qty',
        store=True)

    # Compute Section
    @api.multi
    @api.depends('module_version_ids')
    def compute_module_version_qty(self):
        for module in self:
            module.module_version_qty = len(module.module_version_ids)

    # Custom Section
    @api.model
    def create_if_not_exist(self, name):
        module = self.search([('name', '=', name)])
        if not module:
            module = self.create({'name': name})
        return module
