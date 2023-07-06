# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MasterDetails(models.Model):
    _name = 'masterdetails.masterdetails'
    _description = 'Master Details'

    name = fields.Char(string='Name')
    value = fields.Integer(string='Value')
    value2 = fields.Float(string='Value 2')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
