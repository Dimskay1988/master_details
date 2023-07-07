from odoo import models, fields, api


class Contract(models.Model):
    _name = 'contract.contract'
    _description = 'Contracts'

    name = fields.Char(string='Contract Number')
    description = fields.Text(string='Description')
    acts_ids = fields.One2many('contract.act', 'contract_id', string='Acts')


class Work(models.Model):
    _name = 'contract.work'
    _description = 'Works'

    name = fields.Char(string='Work Name')
    description = fields.Text(string='Work Description')
    quantity = fields.Float(string='Quantity')
    unit = fields.Char(string='Unit of measurement')
    unit_price = fields.Float(string='Unit Price')


class SubWork(models.Model):
    _name = 'contract.subwork'
    _description = 'Sub Works'

    name = fields.Char(string='Sub Work Name')
    description = fields.Text(string='Sub Work Description')
    work_id = fields.Many2one('contract.work', string='Work')


class Act(models.Model):
    _name = 'contract.act'
    _description = 'Acts'

    name = fields.Char(string='Act Number')
    description = fields.Text(string='Description')
    contract_id = fields.Many2one('contract.contract', string='Contract')
    photos = fields.Many2many('ir.attachment', string='Photos')
    work_ids = fields.Many2many('contract.work', string='Works')
    subwork_ids = fields.Many2many('contract.subwork', string='Sub Works')

    def action_add_work(self):
        work = self.env['contract.work'].create({'name': 'New Work'})
        self.work_ids = [(4, work.id)]

    def action_add_subwork(self):
        subwork = self.env['contract.subwork'].create({'name': 'New Sub Work'})
        self.subwork_ids = [(4, subwork.id)]
