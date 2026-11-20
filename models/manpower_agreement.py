from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ManpowerAgreement(models.Model):
    _name = 'manpower.agreement'
    _description = 'Manpower Supply Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end desc, id desc'

    # --- Registration ---
    name = fields.Char(
        string="Agreement Reference", required=True, copy=False,
        default=lambda self: _('New'), tracking=True)
    provider_id = fields.Many2one(
        'res.partner', string="Service Provider", required=True,
        domain=[('is_manpower_provider', '=', True)], tracking=True)
    business_unit_id = fields.Many2one(
        'res.company', string="Receiving Business Unit", required=True,
        default=lambda self: self.env.company, tracking=True)
    agreement_date = fields.Date(string="Agreement Date", required=True, tracking=True)
    date_start = fields.Date(string="Effective Date", required=True, tracking=True)
    date_end = fields.Date(string="Expiration Date", required=True, tracking=True)
    terms = fields.Html(string="Contractual Terms")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ], default='draft', required=True, tracking=True, copy=False)
    previous_agreement_id = fields.Many2one(
        'manpower.agreement', string="Renewed From", copy=False, readonly=True)

    # --- Manpower distribution ---
    manpower_distribution_ids = fields.One2many(
        'manpower.agreement.line', 'agreement_id',
        string="Manpower Distribution", copy=True)
    male_qty = fields.Integer(
        string="Total Male Workers", compute='_compute_manpower_totals',
        store=True, tracking=True)
    female_qty = fields.Integer(
        string="Total Female Workers", compute='_compute_manpower_totals',
        store=True, tracking=True)
    manpower_qty = fields.Integer(
        string="Total Manpower", compute='_compute_manpower_totals',
        store=True, tracking=True)
    
    # --- Amendments ---
    amendment_ids = fields.One2many(
        'manpower.agreement.amendment', 'agreement_id', string="Amendments",
        copy=False)

    # --- Cost and payment ---
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id)
    service_fee = fields.Monetary(string="Service Fee", tracking=True)
    manpower_rate = fields.Monetary(string="Manpower Rate", tracking=True)
    rate_basis = fields.Selection([
        ('person_day', 'Per Person / Day'),
        ('person_month', 'Per Person / Month'),
        ('person_year', 'Per Person / Year'),
        ('lump_sum', 'Lump Sum'),
    ], string="Rate Basis", default='person_month', tracking=True)
    payment_frequency = fields.Selection([
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
    ], string="Payment Frequency", default='monthly', tracking=True)
    other_charges = fields.Monetary(string="Other Contractual Charges", tracking=True)
    payment_terms = fields.Text(string="Payment Terms")

    # --- Renewal ---
    notice_days = fields.Integer(
        string="Notify Before Expiry (days)", default=30, tracking=True)
    responsible_id = fields.Many2one(
        'res.users', string="Responsible", default=lambda self: self.env.user,
        tracking=True)
    expiry_notified = fields.Boolean(copy=False, readonly=True)
    expiring_soon = fields.Boolean(compute='_compute_expiring_soon')

    # --- Documents ---
    documents_count = fields.Integer(compute='_compute_documents_count')

    # ------------------------------------------------------------------
    # Computes and constraints
    # ------------------------------------------------------------------
    @api.depends('state', 'date_end', 'notice_days')
    def _compute_expiring_soon(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.expiring_soon = bool(
                rec.state == 'active' and rec.date_end
                and rec.date_end - timedelta(days=rec.notice_days) <= today)

    def _compute_documents_count(self):
        Document = self.env['documents.document']
        for rec in self:
            rec.documents_count = Document.search_count([
                ('res_model', '=', rec._name), ('res_id', '=', rec.id),
            ]) if rec.id else 0

    @api.depends('manpower_distribution_ids.male_qty',
                 'manpower_distribution_ids.female_qty',
                 'manpower_distribution_ids.total_qty')
    def _compute_manpower_totals(self):
        """Compute total male, female, and overall manpower from distribution lines."""
        for rec in self:
            rec.male_qty = sum(rec.manpower_distribution_ids.mapped('male_qty'))
            rec.female_qty = sum(rec.manpower_distribution_ids.mapped('female_qty'))
            rec.manpower_qty = sum(rec.manpower_distribution_ids.mapped('total_qty'))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_end < rec.date_start:
                raise ValidationError(
                    _("The expiration date cannot be before the effective date."))

    @api.constrains('manpower_distribution_ids')
    def _check_positive(self):
        """Validate manpower quantities through distribution lines."""
        for rec in self:
            # Quantity validation is handled by line constraints
            if rec.notice_days < 0:
                raise ValidationError(_("Notification days cannot be negative."))

    # ------------------------------------------------------------------
    # ORM overrides
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('manpower.agreement')
                    or _('New'))
        return super().create(vals_list)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_confirm(self):
        self.write({'state': 'active'})

    def action_terminate(self):
        self.write({'state': 'terminated'})

    def action_renew(self):
        self.ensure_one()
        new = self.copy({
            'name': _('New'),
            'agreement_date': fields.Date.context_today(self),
            'date_start': self.date_end + timedelta(days=1),
            'date_end': self.date_end + timedelta(days=366),
            'previous_agreement_id': self.id,
            'state': 'draft',
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'manpower.agreement',
            'res_id': new.id,
            'view_mode': 'form',
        }

    def action_open_documents(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Documents'),
            'res_model': 'documents.document',
            'view_mode': 'kanban,list,form',
            'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
            },
        }

    # ------------------------------------------------------------------
    # Scheduled action
    # ------------------------------------------------------------------
    @api.model
    def _cron_check_expiry(self):
        today = fields.Date.context_today(self)

        # 1. Notify responsible users before expiry
        to_check = self.search([
            ('state', '=', 'active'), ('expiry_notified', '=', False)])
        for rec in to_check:
            if rec.date_end < today:
                continue
            if rec.date_end - timedelta(days=rec.notice_days) <= today:
                user = rec.responsible_id or self.env.user
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=rec.date_end,
                    summary=_("Agreement expiring: review and renew"),
                    note=_("Agreement %(ref)s with %(provider)s expires on %(date)s.",
                           ref=rec.name, provider=rec.provider_id.name,
                           date=rec.date_end),
                    user_id=user.id,
                )
                rec.message_post(
                    body=_("This agreement expires on %s. Please review and "
                           "start the renewal or extension procedure.", rec.date_end),
                    partner_ids=user.partner_id.ids,
                    subtype_xmlid='mail.mt_comment',
                )
                rec.expiry_notified = True

        # 2. Mark expired agreements
        self.search([
            ('state', '=', 'active'), ('date_end', '<', today)
        ]).write({'state': 'expired'})
