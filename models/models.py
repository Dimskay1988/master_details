from odoo import models, fields, api
from lxml import etree
import xml.etree.ElementTree as ET


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

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(Act, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                  submenu=submenu)

        if view_type == 'form':
            doc = etree.XML(result['arch'])
            guide_id_field = doc.xpath("//field[@name='guide_id']")
            if guide_id_field:
                guide_id_field = guide_id_field[0]
                parent_eil_nr = self.env.context.get('default_parent_eil_nr')
                if parent_eil_nr:
                    domain = "[('eil_nr', '=', %s)]" % parent_eil_nr
                else:
                    domain = "[]"

                guide_id_field.set('domain', domain)

            result['arch'] = etree.tostring(doc)
        return result


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
    get_group = fields.Selection(selection='_get_group_options', string='ALL group')
    get_group_text = fields.Char(string='Group Text', compute='_compute_get_group_text')
    parent_eil_nr = fields.Float(string='Parent Eil. Nr.', related='guide_id.eil_nr', store=True)

    @api.depends('get_group')
    def _compute_get_group_text(self):
        for record in self:
            if record.get_group:
                guide_id = int(record.get_group.split()[1])
                guide = self.env['contract.guide'].browse(guide_id)
                record.get_group_text = guide.diameter
            else:
                record.get_group_text = ''

    @api.model
    def _get_group_options(self):
        result = []
        count = 0
        all_guides = self.env['contract.guide'].search([])
        for guide in all_guides:
            if guide.eil_nr.is_integer():
                count += 1
                result.append((f'operation {guide.id}', f'{count} {guide.diameter}'))
        return result


class WorkGuide(models.Model):
    _name = 'contract.guide'
    _description = 'WorkGuide'

    eil_nr = fields.Float(string='Eil. Nr.')
    parent_id = fields.Many2one('contract.guide', string='Parent Work')
    group = fields.Char(string='Group')
    diameter = fields.Char(string='Diameter')
    operations = fields.Text(string='Operations')
    unit = fields.Char(string='Unit')
    quantity = fields.Float(string='Quantity')
    materials = fields.Float(string='Materials')
    works = fields.Float(string='Works')
    mechanisms = fields.Float(string='Mechanical')
    total_cost = fields.Float(string='Common unit excluding VAT')
    total = fields.Float(string='Total including VAT')

    def name_get(self):
        result = []
        all_records = self.search([])
        for record in all_records:
            result.append((record.id, f'{record.eil_nr} {record.diameter}'))
        return result

    def print_report(self):
        return self.env.ref('your_module.report_contract_guide').report_action(self)


def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    result = super(Act, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

    if view_type == 'form':
        doc = ET.fromstring(result['arch'])
        guide_id_field = doc.find(".//field[@name='guide_id']")
        if guide_id_field is not None:
            parent_eil_nr = self.env.context.get('default_parent_eil_nr')
            if parent_eil_nr:
                domain = "[('eil_nr', '=', %s)]" % parent_eil_nr
            else:
                domain = "[]"

            guide_id_field.set('domain', domain)

        result['arch'] = ET.tostring(doc, encoding='unicode')

    return result
