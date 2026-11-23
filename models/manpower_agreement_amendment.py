from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ManpowerAgreementAmendment(models.Model):
    _name = 'manpower.agreement.amendment'
    _description = 'Manpower Agreement Amendment'
    _order = 'date desc, id desc'

    agreement_id = fields.Many2one(
        'manpower.agreement', required=True, ondelete='cascade')
    date = fields.Date(default=fields.Date.context_today, required=True)
    previous_qty = fields.Integer(string="Previous Quantity", readonly=True)
    new_qty = fields.Integer(string="New Quantity", readonly=True,
                             compute='_compute_new_qty', store=True)
    reason = fields.Char(string="Reason / Amendment Reference")
    approved_by_id = fields.Many2one(
        'res.users', string="Approved By", default=lambda self: self.env.user)
    
    # Amendment distribution lines
    amendment_line_ids = fields.One2many(
        'manpower.agreement.amendment.line', 'amendment_id',
        string="Amendment Lines")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        agreement_id = res.get('agreement_id') or self.env.context.get('default_agreement_id')
        if agreement_id:
            agreement = self.env['manpower.agreement'].browse(agreement_id)
            if 'previous_qty' in fields_list:
                res['previous_qty'] = agreement.manpower_qty
            if 'amendment_line_ids' in fields_list and not res.get('amendment_line_ids'):
                lines = []
                for dist in agreement.manpower_distribution_ids:
                    lines.append((0, 0, {
                        'category_id': dist.category_id.id,
                        'previous_male_qty': dist.male_qty,
                        'previous_female_qty': dist.female_qty,
                        'male_qty': dist.male_qty,
                        'female_qty': dist.female_qty,
                    }))
                if lines:
                    res['amendment_line_ids'] = lines
        return res

    @api.onchange('agreement_id')
    def _onchange_agreement_id(self):
        if self.agreement_id:
            self.previous_qty = self.agreement_id.manpower_qty
            if not self.amendment_line_ids and self.agreement_id.manpower_distribution_ids:
                lines = []
                for dist in self.agreement_id.manpower_distribution_ids:
                    lines.append((0, 0, {
                        'category_id': dist.category_id.id,
                        'previous_male_qty': dist.male_qty,
                        'previous_female_qty': dist.female_qty,
                        'male_qty': dist.male_qty,
                        'female_qty': dist.female_qty,
                    }))
                self.amendment_line_ids = lines

    @api.depends('amendment_line_ids.male_qty', 'amendment_line_ids.female_qty')
    def _compute_new_qty(self):
        """Compute new quantity from amendment lines."""
        for rec in self:
            rec.new_qty = sum(
                line.male_qty + line.female_qty 
                for line in rec.amendment_line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        """Record the previous quantity and update agreement distribution."""
        for vals in vals_list:
            agreement_id = vals.get('agreement_id') or self.env.context.get('default_agreement_id')
            if agreement_id:
                if 'agreement_id' not in vals:
                    vals['agreement_id'] = agreement_id
                if not vals.get('previous_qty'):
                    agreement = self.env['manpower.agreement'].browse(agreement_id)
                    vals['previous_qty'] = agreement.manpower_qty
        
        records = super().create(vals_list)
        
        for rec in records:
            # Apply amendment lines to agreement distribution
            if rec.amendment_line_ids:
                rec._apply_amendment_to_agreement()
                rec.agreement_id.message_post(
                    body=_("Manpower distribution amended from %(previous)s to %(new)s workers. %(reason)s",
                           previous=rec.previous_qty,
                           new=rec.new_qty,
                           reason=rec.reason or ''))
        return records

    def write(self, vals):
        """Update agreement distribution when amendment lines change."""
        res = super().write(vals)
        if 'amendment_line_ids' in vals:
            for rec in self:
                if rec.amendment_line_ids:
                    rec._apply_amendment_to_agreement()
                    rec.agreement_id.message_post(
                        body=_("Manpower distribution amended from %(previous)s to %(new)s workers. %(reason)s",
                               previous=rec.previous_qty,
                               new=rec.new_qty,
                               reason=rec.reason or ''))
        return res

    def _apply_amendment_to_agreement(self):
        """Apply amendment lines to agreement's distribution lines."""
        self.ensure_one()
        agreement = self.agreement_id
        
        # Update or create distribution lines based on amendment
        for amend_line in self.amendment_line_ids:
            existing_line = agreement.manpower_distribution_ids.filtered(
                lambda l: l.category_id == amend_line.category_id)
            
            if existing_line:
                existing_line.write({
                    'male_qty': amend_line.male_qty,
                    'female_qty': amend_line.female_qty,
                })
            else:
                self.env['manpower.agreement.line'].create({
                    'agreement_id': agreement.id,
                    'category_id': amend_line.category_id.id,
                    'male_qty': amend_line.male_qty,
                    'female_qty': amend_line.female_qty,
                })


class ManpowerAgreementAmendmentLine(models.Model):
    _name = 'manpower.agreement.amendment.line'
    _description = 'Manpower Agreement Amendment Line'
    _order = 'amendment_id, category_id'

    amendment_id = fields.Many2one(
        'manpower.agreement.amendment', required=True, ondelete='cascade')
    category_id = fields.Many2one(
        'manpower.service.category', string="Service Category",
        required=True, domain=[('active', '=', True)])
    previous_male_qty = fields.Integer(string="Previous Male", readonly=True)
    previous_female_qty = fields.Integer(string="Previous Female", readonly=True)
    male_qty = fields.Integer(string="New Male", default=0)
    female_qty = fields.Integer(string="New Female", default=0)
    total_qty = fields.Integer(
        string="New Total", compute='_compute_total_qty', store=True)

    _sql_constraints = [
        ('amendment_category_unique',
         'UNIQUE(amendment_id, category_id)',
         'A service category can only appear once per amendment.')
    ]

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id:
            agreement = self.amendment_id.agreement_id or (
                self.env['manpower.agreement'].browse(self.env.context.get('default_agreement_id'))
                if self.env.context.get('default_agreement_id') else False
            )
            if agreement:
                existing = agreement.manpower_distribution_ids.filtered(
                    lambda l: l.category_id == self.category_id
                )
                if existing:
                    self.previous_male_qty = existing[0].male_qty
                    self.previous_female_qty = existing[0].female_qty
                    if not self.male_qty and not self.female_qty:
                        self.male_qty = existing[0].male_qty
                        self.female_qty = existing[0].female_qty
                else:
                    self.previous_male_qty = 0
                    self.previous_female_qty = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('category_id'):
                amend = self.env['manpower.agreement.amendment'].browse(vals.get('amendment_id')) if vals.get('amendment_id') else False
                agreement = amend.agreement_id if amend else (
                    self.env['manpower.agreement'].browse(self.env.context.get('default_agreement_id'))
                    if self.env.context.get('default_agreement_id') else False
                )
                if agreement:
                    cat_id = vals['category_id']
                    dist = agreement.manpower_distribution_ids.filtered(lambda l: l.category_id.id == cat_id)
                    if dist:
                        if 'previous_male_qty' not in vals or not vals.get('previous_male_qty'):
                            vals['previous_male_qty'] = dist[0].male_qty
                        if 'previous_female_qty' not in vals or not vals.get('previous_female_qty'):
                            vals['previous_female_qty'] = dist[0].female_qty
        return super().create(vals_list)

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
