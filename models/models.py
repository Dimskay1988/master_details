from odoo import models, fields, api
from lxml import etree
import xml.etree.ElementTree as ET


class Contract(models.Model):
    _name = 'contract.contract'
    _description = 'Contracts'

    name = fields.Char(string='Contract Number')
    short_description = fields.Char(string="short description")
    contract_id = fields.Many2one('contract.contract', string='Contract')
    description = fields.Text(string='Description')
    create_date = fields.Datetime(string='Create Date', readonly=True, default=lambda self: fields.Datetime.now())
    write_date = fields.Datetime(string='Write Date', readonly=True)
    client = fields.Many2one('res.partner', string='Client', domain="[('is_company', '=', True)]")
    subcontractor = fields.Many2one('res.partner', string='Subcontractor', domain="[('is_company', '=', True)]")
    acts_ids = fields.One2many('contract.act', 'contract_id', string='Acts')
    work_ids = fields.One2many('contract.work', 'contract_id', string='Works')

    def write(self, values):
        values['write_date'] = fields.Datetime.now()
        return super(Contract, self).write(values)

    def generate_report_data(self):
        print("Generating")
        report_data = []
        for contract in self:
            contract_data = {
                'name': contract.name,
                'short_description': contract.short_description,
                'client_name': contract.client.name,
                'subcontractor_name': contract.subcontractor.name,
                'works': []
            }
            for work in contract.work_ids:
                work_data = {
                    'eil_nr': work.guide_id.eil_nr,
                    'diameter': work.guide_id.diameter,
                    'operations': work.guide_id.operations,
                    'unit': work.guide_id.unit,
                    'quantity': work.quantity,
                    'materials': work.guide_id.materials,
                    'works': work.guide_id.works,
                    'total': work.guide_id.total,
                }
                contract_data['works'].append(work_data)
            report_data.append(contract_data)
        return report_data


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
    address = fields.Char(string='Address')
    master_id = fields.Many2one('hr.employee', string='Master')
    phone_number = fields.Text(string='Phone Number')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    date_receipt_work = fields.Date(string='Date of receipt of work')
    preliminary_dismantling = fields.Integer(string='Ardomas preliminarus dangų plotas')
    permission_excavate = fields.Selection(selection=PERMISSION_SELECTION, string='Permission to excavate')
    contract_id = fields.Many2one('contract.contract', string='Contract')
    work_ids = fields.One2many('contract.work', 'act_id', string='Works')
    photos = fields.Many2many('ir.attachment', string='Photos')
    employers_ids = fields.Many2many('hr.employee', string='Employees')
    total_works_cost = fields.Float(string='Total Works Cost', compute='_compute_total_works_cost')
    vat_amount = fields.Float(string='VAT Amount', compute='_compute_vat_amount')
    total_amount_with_vat = fields.Float(string='Total Amount with VAT', compute='_compute_total_amount_with_vat')
    subcontractor_name = fields.Char(string='Subcontractor Name', compute='_compute_subcontractor_name', store=True)
    client_name = fields.Char(string='Client Name', compute='_compute_client_name', store=True)

    @api.depends('contract_id.subcontractor', 'contract_id.subcontractor.name')
    def _compute_subcontractor_name(self):
        for act in self:
            act.subcontractor_name = act.contract_id.subcontractor.name if act.contract_id.subcontractor else ''

    @api.depends('contract_id.client', 'contract_id.client.name')
    def _compute_client_name(self):
        for act in self:
            act.client_name = act.contract_id.client.name if act.contract_id.client else ''
    @api.depends('work_ids.only_in_euro_without_vat')
    def _compute_total_works_cost(self):
        for act in self:
            act.total_works_cost = round(sum(work.only_in_euro_without_vat for work in act.work_ids), 2)

    @api.depends('total_works_cost')
    def _compute_vat_amount(self):
        for act in self:
            act.vat_amount = round(act.total_works_cost * 0.21, 2)

    @api.depends('total_works_cost', 'vat_amount')
    def _compute_total_amount_with_vat(self):
        for act in self:
            act.total_amount_with_vat = round(act.total_works_cost + act.vat_amount, 2)

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
    contract_id = fields.Many2one('contract.contract', string='Contract')
    description_precipitation = fields.Text(string='Description of precipitation')
    employers_ids = fields.Many2many('hr.employee', string='Employees', relation='act_employers_rel')
    guide_id = fields.Many2one('contract.guide', string='Work Guide')
    get_group = fields.Selection(selection='_get_group_options', string='ALL group')
    get_group_text = fields.Char(string='Group Text', compute='_compute_get_group_text')
    parent_eil_nr = fields.Float(string='Parent Eil. Nr.', related='guide_id.eil_nr', store=True)
    total_unit_price_without_vat = fields.Float(string='Total Unit Price Without VAT',
                                                compute='_compute_total_unit_price')
    only_in_euro_without_vat = fields.Float(string='Only in euro without VAT',
                                            compute='_compute_total_in_euro')

    @api.depends('total_unit_price_without_vat', 'quantity')
    def _compute_total_in_euro(self):
        for work in self:
            total_price = round(work.total_unit_price_without_vat * work.quantity, 2)
            work.only_in_euro_without_vat = total_price if work.quantity and work.total_unit_price_without_vat else 0.0

    @api.depends('guide_id', 'guide_id.materials', 'guide_id.works', 'guide_id.mechanisms')
    def _compute_total_unit_price(self):
        for work in self:
            total_price = 0.0
            if work.guide_id:
                total_price += work.guide_id.materials
                total_price += work.guide_id.works
                total_price += work.guide_id.mechanisms
            work.total_unit_price_without_vat = round(total_price, 2)

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
    contract_id = fields.Many2one('contract.contract', string='Contract')
    act_id = fields.Many2one('contract.act', string='Act')

    @api.model
    def create(self, vals):
        # Round the values before creating the record
        vals['materials'] = round(vals.get('materials', 0.0), 2)
        vals['works'] = round(vals.get('works', 0.0), 2)
        vals['mechanisms'] = round(vals.get('mechanisms', 0.0), 2)
        return super(WorkGuide, self).create(vals)

    def write(self, vals):
        # Round the values before updating the record
        if 'materials' in vals:
            vals['materials'] = round(vals['materials'], 2)
        if 'works' in vals:
            vals['works'] = round(vals['works'], 2)
        if 'mechanisms' in vals:
            vals['mechanisms'] = round(vals['mechanisms'], 2)
        return super(WorkGuide, self).write(vals)


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
