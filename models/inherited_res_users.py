from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("propiedades", "buyer")
