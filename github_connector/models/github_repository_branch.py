# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import os

from subprocess import check_output
from datetime import datetime

from openerp import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)


class GithubRepository(models.Model):
    _name = 'github.repository.branch'
    _inherit = ['abstract.github.model']
    _order = 'complete_name'

    _github_type = 'repository_branches'
    _github_login_field = False

    _SELECTION_STATE = [
        ('to_download', 'To Download'),
        ('to_analyze', 'To Analyze'),
        ('analyzed', 'Analyzed'),
    ]

    # Column Section
    name = fields.Char(
        string='Name', readonly=True, select=True)

    size = fields.Integer(
        string='Size (Byte) ', readonly=True)

    mb_size = fields.Float(
        string='Size (Megabyte)', store=True, compute='_compute_mb_size')

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

    local_path = fields.Char(
        string='Local Path', compute='_compute_local_path')

    state = fields.Selection(
        string='State', selection=_SELECTION_STATE, default='to_download')

    last_download_date = fields.Datetime(string='Last Download Date')

    last_analyze_date = fields.Datetime(string='Last Analyze Date')

    # Action Section
    @api.multi
    def button_download_code(self):
        return self._download_code()

    @api.multi
    def button_analyze_code(self):
        return self._analyze_code()

    def cron_download_all(self):
        branches = self.search([])
        branches._download_code()
        return True

    def cron_analyze_all(self):
        branches = self.search([])
        branches._analyze_code()
        return True

    # Custom
    def create_or_update_from_name(self, repository_id, name):
        branch = self.search([
            ('name', '=', name), ('repository_id', '=', repository_id)])
        if not branch:
            branch = self.create({
                'name': name, 'repository_id': repository_id})
        return branch

    @api.multi
    def _download_code(self):
        for branch in self:
            if not os.path.exists(branch.local_path):
                _logger.info(
                    "Cloning new repository into %s ..." % (branch.local_path))
                # Cloning the repository
                os.makedirs(branch.local_path)

                # TODO move this url in github.py file
                command = "cd %s &&"\
                    + "git clone https://github.com/%s/%s.git -b %s ." % (
                        branch.local_path,
                        branch.repository_id.organization_id.github_login,
                        branch.repository_id.name,
                        branch.name)
                os.system(command)
                branch.write({
                    'last_download_date': datetime.today(),
                    'state': 'to_analyze',
                    })
            else:
                # Update repository
                _logger.info(
                    "Pulling existing repository %s ..." % (branch.local_path))
                try:
                    res = check_output(
                        ['git', 'pull', 'origin', branch.name],
                        cwd=branch.local_path)
                except:
                    raise exceptions.Warning(
                        _("Git Access Error"),
                        _("Unable to access to pull repository in %s.") % (
                            branch.local_path))
                if branch.state == 'to_download' or\
                        'up-to-date' not in res:
                    branch.write({
                        'last_download_date': datetime.today(),
                        'state': 'to_analyze',
                        })
                else:
                    branch.write({
                        'last_download_date': datetime.today(),
                        })
        return True

    def _get_analyzable_files(self, existing_folder):
        res = []
        for root, dirs, files in os.walk(existing_folder):
            if '/.git' not in root:
                for fic in files:
                    if fic != '.gitignore':
                        res.append(os.path.join(root, fic))
        return res

    @api.multi
    def _analyze_code(self):
        """Overload Me in custom Module that manage Source Code analysis.
        """
        for branch in self:
            if not os.path.exists(branch.local_path):
                _logger.warning(
                    "Warning Folder %s not found. Analyze skipped." % (
                        branch.local_path))
            else:
                _logger.info(
                    "Analyzing Source Code in %s ..." % (branch.local_path))
                size = 0
                for file_path in self._get_analyzable_files(branch.local_path):
                        size += os.path.getsize(file_path)
                branch.write({
                    'last_analyze_date': datetime.today(),
                    'state': 'analyzed',
                    'size': size,
                })
        return True

    # Compute Section
    @api.multi
    @api.depends('name', 'repository_id.name')
    def _compute_complete_name(self):
        for branch in self:
            branch.complete_name =\
                branch.repository_id.name + '/' + branch.name

    @api.multi
    @api.depends('size')
    def _compute_mb_size(self):
        for branch in self:
            branch.mb_size = float(branch.size) / (1024 ** 2)

    @api.multi
    @api.depends('organization_id', 'name')
    def _compute_organization_serie_id(self):
        for branch in self:
            for serie in branch.organization_id.organization_serie_ids:
                if serie.name == branch.name:
                    branch.organization_serie_id = serie

    @api.multi
    @api.depends('complete_name')
    def _compute_local_path(self):
        path = self.env['ir.config_parameter'].get_param(
            'github.source_code_local_path')
        for branch in self:
            branch.local_path = path\
                + branch.repository_id.organization_id.github_login + '/'\
                + branch.complete_name
