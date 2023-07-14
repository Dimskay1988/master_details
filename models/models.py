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
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    date_receipt_work = fields.Date(string='Date of receipt of work')
    preliminary_dismantling = fields.Integer(string='Ardomas preliminarus dangų plotas')
    permission_excavate = fields.Selection(selection=PERMISSION_SELECTION, string='Permission to excavate')
    work_ids = fields.One2many('contract.work', 'act_id', string='Works')
    photos = fields.Many2many('ir.attachment', string='Photos')
    employers_ids = fields.Many2many('hr.employee', string='Employees')

    def action_add_work(self):
        view_id = self.env.ref('master_detail.work_guide_form_view').id
        return {
            'name': 'Add Work',
            'view_mode': 'form',
            'res_model': 'contract.work',
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_act_id': self.id,
                'default_employers_ids': [(6, 0, self.employers_ids.ids)],
            }
        }


class Work(models.Model):
    _name = 'contract.work'
    _description = 'Repair Works'

    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity')
    unit = fields.Char(string='Unit of measurement')
    act_id = fields.Many2one('contract.act', string='Act')
    description_precipitation = fields.Text(string='Description of precipitation')
    employers_ids = fields.Many2many('hr.employee', string='Employees', relation='act_employers_rel')
    guide_id = fields.Many2one('contract.guide', string='Work Guide')
    get_group = fields.Char(string='ALL group', compute='_get_group', store=True)

    @api.depends('guide_id', 'guide_id.diameter')
    def _get_group(self):
        for record in self:
            result = []
            all_group = self.env['contract.guide']
            all_records = all_group.search([])
            for guide in all_records:
                if guide.eil_nr.is_integer():
                    result.append(guide.diameter)
            record.get_group = ', '.join(result)


class WorkGuide(models.Model):
    _name = 'contract.guide'
    _description = 'WorkGuide'

    eil_nr = fields.Float(string='Eil. Nr.')
    parent_id = fields.Many2one('contract.guide', string='Parent Work')
    group = fields.Char(string='Group')
    diameter = fields.Char(string='Diameter')
    operations = fields.Text(string='Operations')

    def name_get(self):
        result = []
        all_records = self.search([])
        for record in all_records:
            if record.eil_nr.is_integer():
                print(record.eil_nr)
                result.append((record.id, record.diameter))
        return result

