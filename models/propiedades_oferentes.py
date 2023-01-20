from odoo import api, models, fields
from odoo.tools import date_utils


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
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        default=lambda self: date_utils.add(fields.Datetime.now(), days=7),
        compute="_compute_date",
        inverse="_inverse_date",
    )

    @api.depends("validity")
    def _compute_date(self):
        for record in self:
            record.validity = 10
            # record.validity = date_utils.add(
            #     fields.Datetime.now(), days=record.validity
            # )

    def _inverse_date(self):
        for record in self:
            record.validity = 48


# class Partner(models.Model):
#     _inherit = "res.partner"

#     property_algo = fields.Many2one()
