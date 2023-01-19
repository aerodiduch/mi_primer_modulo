from odoo import fields, models
from odoo.tools import date_utils


class Propiedades(models.Model):
    _name = "propiedades"
    _description = "mi primer modulo"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=date_utils.add(fields.Datetime.now(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    property_type = fields.Many2one("propiedades.tipo", string="Property Type")
    salesperson = fields.Many2one(
        "res.partner", string="Salesman", default=lambda self: self.env.user.partner_id
    )
    buyer = fields.Many2one("res.users", string="Buyer", copy=False)
    tags_ids = fields.Many2many("propiedades.tagss")
    offer_ids = fields.One2many(
        "propiedades.oferentes", "partner_id", string="Ofertas Recibidas"
    )
