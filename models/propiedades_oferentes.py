from odoo import models, fields


class Oferentes(models.Model):
    _name = "propiedades.oferentes"
    _description = "Oferentes de propiedades"

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("propiedades", required=True)
