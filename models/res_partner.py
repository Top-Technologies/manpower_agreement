from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_manpower_provider = fields.Boolean(string="Manpower Provider", tracking=True)
    manpower_agreement_ids = fields.One2many(
        'manpower.agreement', 'provider_id', string="Manpower Agreements")
    manpower_agreement_count = fields.Integer(
        compute='_compute_manpower_agreement_count')
    
    # Provider-level manpower summaries (active agreements only)
    active_male_qty = fields.Integer(
        string="Active Male Workers", compute='_compute_active_manpower',
        help="Total male workers under active agreements")
    active_female_qty = fields.Integer(
        string="Active Female Workers", compute='_compute_active_manpower',
        help="Total female workers under active agreements")
    active_manpower_qty = fields.Integer(
        string="Active Total Manpower", compute='_compute_active_manpower',
        help="Total workers under active agreements")

    def _compute_manpower_agreement_count(self):
        for partner in self:
            partner.manpower_agreement_count = len(partner.manpower_agreement_ids)

    @api.depends('manpower_agreement_ids.state',
                 'manpower_agreement_ids.male_qty',
                 'manpower_agreement_ids.female_qty',
                 'manpower_agreement_ids.manpower_qty')
    def _compute_active_manpower(self):
        """Compute provider's total manpower from active agreements."""
        for partner in self:
            active_agreements = partner.manpower_agreement_ids.filtered(
                lambda a: a.state == 'active')
            partner.active_male_qty = sum(active_agreements.mapped('male_qty'))
            partner.active_female_qty = sum(active_agreements.mapped('female_qty'))
            partner.active_manpower_qty = sum(active_agreements.mapped('manpower_qty'))

    def action_view_manpower_agreements(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manpower Agreements',
            'res_model': 'manpower.agreement',
            'view_mode': 'list,form',
            'domain': [('provider_id', '=', self.id)],
            'context': {'default_provider_id': self.id},
        }
