from odoo import models, fields, api


class Contract(models.Model):
    _name = 'contract.contract'
    _description = 'Contracts'

    name = fields.Char(string='Contract Number')
    description = fields.Text(string='Description')
    acts_ids = fields.One2many('contract.act', 'contract_id', string='Acts')


class Act(models.Model):
    _name = 'contract.act'
    _description = 'Acts'

    name = fields.Char(string='Act Number')
    description = fields.Text(string='Description')
    contract_id = fields.Many2one('contract.contract', string='Contract')