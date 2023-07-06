# -*- coding: utf-8 -*-

from odoo import models, fields, api


class master_details(models.Model):
    _name = 'master_details.master_details'
    _description = 'master_details.master_details'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
