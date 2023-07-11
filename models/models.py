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

    REPAIR_WORKS_SELECTION = [
        ('1', 'Trūkimo vietos užtaisymas, kai gylis iki 2,0 m., plieninio vamzdžio skersmuo'),
        ('2', 'Trūkimo vietos užtaisymas, kai gylis iki 2,5 m., plieninio vamzdžio skersmuo'),
        ('3', 'Trūkimo vietos užtaisymas, kai gylis iki 3,0 m., plieninio vamzdžio skersmuo'),
        ('4', 'Trūkimo vietos užtaisymas, kai gylis iki 4,0 m., plieninio vamzdžio skersmuo'),
        ('5', 'Trūkimo vietos užtaisymas, kai gylis iki 5,0 m., plieninio vamzdžio skersmuo'),
        ('6', 'Trūkimo vietos užtaisymas, kai gylis iki 6,0 m., plieninio vamzdžio skersmuo'),
        ('7', 'Vamzdžio movos sandarinimas, kai gylis iki 2,0 m., ketinio vamdžio skersmuo, mm'),
        ('8', 'Vamzdžio movos sandarinimas, kai gylis iki 2,5 m., ketinio vamdžio skersmuo, mm'),
        ('9', 'Vamzdžio movos sandarinimas, kai gylis iki 3,0 m., ketinio vamdžio skersmuo, mm'),
        ('10', 'Vamzdžio movos sandarinimas, kai gylis iki 4,0 m., ketinio vamdžio skersmuo, mm'),
        ('11', 'Remontinės sudedamos movos uždėjimas, kai gylis iki 2,0 m. ketinio vamzdžio skersmuo, mm'),
        ('12', 'Remontinės sudedamos movos uždėjimas, kai gylis iki 2,5 m. ketinio vamzdžio skersmuo, mm'),
        ('13', 'Remontinės sudedamos movos uždėjimas, kai gylis iki 3,0 m. ketinio vamzdžio skersmuo, mm'),
        ('14', 'Remontinės sudedamos movos uždėjimas, kai gylis iki 4,0 m. ketinio vamzdžio skersmuo, mm'),
        ('15', 'Vamzdžio pažeistos dalies keitimas, kai gylis iki 2,0 m., ketinio vamdžio skersmuo, mm'),
        ('16', 'Vamzdžio pažeistos dalies keitimas, kai gylis iki 2,5 m., ketinio vamdžio skersmuo, mm'),
        ('17', 'Vamzdžio pažeistos dalies keitimas, kai gylis iki 3,0 m., ketinio vamdžio skersmuo, mm'),
        ('18', 'Vamzdžio pažeistos dalies keitimas, kai gylis iki 4,0 m., ketinio vamdžio skersmuo, mm'),
        ('19', 'Vamzdžio pažeistos dalies keitimas, kai gylis iki 2,0 m, polietileninio vamdžio skersmuo, mm'),
        ('20', 'Vamzdžio pažeistos dalies keitimas, kai gylis iki 2,5 m, polietileninio vamdžio skersmuo, mm'),
    ]

    diameter_selection = [
        ('32', '32'),
        ('40', '40'),
        ('50', '50'),
        ('63', '63'),
        ('80', '80'),
        ('100', '100'),
        ('110', '110'),
        ('125', '125'),
        ('150', '150'),
        ('200', '200'),
        ('250', '250'),
        ('300', '300'),
        ('350', '350'),
        ('400', '400'),
        ('500', '500'),
        ('600', '600'),
        ('700', '700'),
        ('800', '800'),
    ]

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
    diameter = fields.Selection(selection=diameter_selection, string='Pipe Diameter ⌀')
    repair_works = fields.Selection(selection=REPAIR_WORKS_SELECTION, string='Repair Works')
