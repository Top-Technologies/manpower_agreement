from odoo import _, fields, models
from odoo.exceptions import UserError


class ManpowerServiceCategory(models.Model):
    _name = 'manpower.service.category'
    _description = 'Manpower Service Category'
    _order = 'sequence, name'

    name = fields.Char(string="Category Name", required=True, translate=True)
    code = fields.Char(string="Code")
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)',
         'The category code must be unique.')
    ]

    def unlink(self):
        """Prevent deletion of categories used in distribution lines."""
        if self.env['manpower.agreement.line'].search_count(
                [('category_id', 'in', self.ids)], limit=1):
            raise UserError(_(
                "Cannot delete service categories that are used in manpower "
                "distribution lines. Archive them instead."))
        return super().unlink()
