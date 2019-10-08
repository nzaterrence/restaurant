# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import datetime


# from odoo.exceptions import ValidationError


class ProductTemplatePos(models.Model):
    _inherit = 'product.template'
    product_attribute_model_ids = fields.One2many('product.attribute.setting', 'template_id')
    qty_account_day = fields.Integer('每日数量',index=True, default=0)

class ProductAttributeSetting(models.Model):
    _name = "product.attribute.setting"
    _description = "Product Attribute Setting"
    template_id = fields.Many2one('product.template')
    name = fields.Char('名称')



