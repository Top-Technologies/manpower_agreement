from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ManpowerAgreementLine(models.Model):
    _name = 'manpower.agreement.line'
    _description = 'Manpower Distribution Line'
    _order = 'agreement_id, category_id'

    agreement_id = fields.Many2one(
        'manpower.agreement', string="Agreement", required=True,
        ondelete='cascade', index=True)
    category_id = fields.Many2one(
        'manpower.service.category', string="Service Category",
        required=True, domain=[('active', '=', True)])
    male_qty = fields.Integer(string="Male Workers", default=0)
    female_qty = fields.Integer(string="Female Workers", default=0)
    total_qty = fields.Integer(
        string="Total Workers", compute='_compute_total_qty',
        store=True, readonly=True)
    notes = fields.Text(string="Notes")

    _sql_constraints = [
        ('agreement_category_unique',
         'UNIQUE(agreement_id, category_id)',
         'A service category can only appear once per agreement.')
    ]

    @api.depends('male_qty', 'female_qty')
    def _compute_total_qty(self):
        for line in self:
            line.total_qty = line.male_qty + line.female_qty

    @api.constrains('male_qty', 'female_qty')
    def _check_quantities(self):
        for line in self:
            if line.male_qty < 0:
                raise ValidationError(
                    _("Male worker quantity cannot be negative."))
            if line.female_qty < 0:
                raise ValidationError(
                    _("Female worker quantity cannot be negative."))
