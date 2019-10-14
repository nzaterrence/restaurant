# -*- coding: utf-8 -*-
# Copyright 2019 Sunflower IT (http://sunflowerweb.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    pos_config_id = fields.Many2one('pos.config', 'Pos Config')
    pos_delete_order = fields.Boolean('Delete pos orders', default=0)
