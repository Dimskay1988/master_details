from odoo import models, fields, api


class Contract(models.Model):
    _name = 'contract.contract'
    _description = 'Contracts'

    name = fields.Char(string='Contract Number')
    description = fields.Text(string='Description')
    create_date = fields.Datetime(string='Create Date', readonly=True, default=lambda self: fields.Datetime.now())
    write_date = fields.Datetime(string='Write Date', readonly=True)
    client = fields.Many2one('res.partner', string='Client', domain="[('is_company', '=', True)]")
    subcontractor = fields.Many2one('res.partner', string='Subcontractor', domain="[('is_company', '=', True)]")
    acts_ids = fields.One2many('contract.act', 'contract_id', string='Acts')

    def write(self, values):
        values['write_date'] = fields.Datetime.now()
        return super(Contract, self).write(values)


class Act(models.Model):
    _name = 'contract.act'
    _description = 'Acts'

    PERMISSION_SELECTION = [
        ('permission', 'Have permission'),
        ('no_permission', 'No permission'),
        ('no_record', 'Missing entry')
    ]

    name = fields.Char(string='Act Number')
    description = fields.Text(string='Description')
    contract_id = fields.Many2one('contract.contract', string='Contract')
    address = fields.Char(string='Address')
    master_id = fields.Many2one('hr.employee', string='Master')
    phone_number = fields.Text(string='Phone Number')
    date_receipt_work = fields.Date(string='Date of receipt of work')
    preliminary_dismantling = fields.Integer(string='Ardomas preliminarus dangų plotas')
    permission_excavate = fields.Selection(selection=PERMISSION_SELECTION, string='Permission to excavate')
    work_ids = fields.One2many('contract.work', 'act_id', string='Works')


class Work(models.Model):
    _name = 'contract.work'
    _description = 'Repair Works'

    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity')
    coverage_type = fields.Char(string='Coverage Type')
    unit = fields.Char(string='Unit of measurement')
    unit_price = fields.Float(string='Unit Price')
    # photos = fields.Many2many('ir.attachment', string='Photos')
    # employers_ids = fields.Many2many('hr.employee', string='Employees', relation='act_employers_rel')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    act_id = fields.Many2one('contract.act', string='Act')
    precipitation_date = fields.Date(string='Precipitation Date')
    description_precipitation = fields.Text(string='Description of precipitation')
    reference_ids = fields.Many2many('contract.reference', string='References')
    job_id = fields.Many2one('contract.job', string='Job')


class Jobs(models.Model):
    _name = 'contract.job'
    _description = 'Jobs'

    name = fields.Char(string='Name of job')
    work_id = fields.Many2one('contract.work', string='Work')
    group_ids = fields.One2many('contract.group', 'job_id', string='Groups')


class GroupJobs(models.Model):
    _name = 'contract.group'
    _description = 'GroupJobs'

    description = fields.Text(string='Description')
    diameter = fields.Char(string='Diameter')
    job_id = fields.Many2one('contract.job', string='Job')
