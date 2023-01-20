from odoo import api, fields, models
from odoo.tools import date_utils


class Propiedades(models.Model):
    _name = "propiedades"
    _description = "mi primer modulo"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: date_utils.add(fields.Datetime.now(), months=3)
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
        "propiedades.oferentes", "property_id", string="Ofertas Recibidas"
    )
    # offer_ids.price ????
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped("offer_ids.price"), default=0)
