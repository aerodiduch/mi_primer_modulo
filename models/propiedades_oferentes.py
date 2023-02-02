from odoo import api, models, fields
from odoo.tools import date_utils
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class Oferentes(models.Model):
    _name = "propiedades.oferentes"
    _description = "Oferentes de propiedades"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("propiedades", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type", store=True)

    validity = fields.Integer(
        compute="_compute_validity", inverse="_inverse_validity", default=7
    )

    date_deadline = fields.Date(
        default=lambda self: date_utils.add(fields.Datetime.now(), days=7),
        compute="_compute_date",
        inverse="_inverse_date",
    )

    _sql_constraints = [
        (
            "check_valid_price",
            "CHECK(price > 0)",
            "Offer price must be strictly positive",
        )
    ]

    @api.model  # pendiente hacer la comprobacion de que no pude ser una oferta mas barata que la anterior
    def create(self, vals):
        property = self.env["propiedades"].browse(vals["property_id"])
        property.state = "offer_received"
        property.write({"state": property.state})
        return super().create(vals)

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            difference = record.date_deadline - date.today()
            self.validity = difference.days

    @api.depends("validity")
    def _compute_date(self):
        for record in self:
            record.date_deadline = date.today() + relativedelta(days=record.validity)

    def _inverse_validity(self):
        pass

    def _inverse_date(self):
        pass

    # from propiedaes.oferentes
    @api.constrains("price")
    def action_confirm(self):
        # Revisar. Creo que la constrain está al reves.
        if self.property_id.expected_price < (self.price * 0.9):
            raise ValidationError(
                "Selling price cannot be lower than 90% of expected price."
            )
        else:

            self.status = "accepted"
            self.property_id.selling_price = self.price
        # Pendiente hacer lo de setear el comprador. No creo que sea my dificil. Es una gansada
        # Muy probable que haya un conflicto entre res.users y res.partner. Sin duda
        #  self.property_id.buyer = self.partner_id
        return True

    def action_cancel(self):
        self.status = "refused"
        return True

    # def _inverse_date(self):
    #     for propiedad in self:
    #         if propiedad.date_deadline:
    #             difference = self.date_deadline - date.today()
    #             propiedad.validity = difference.days
    #             print("Hola!")


# from odoo import api, models, fields
# from odoo.tools import date_utils


# class Oferentes(models.Model):
#     _name = "propiedades.oferentes"
#     _description = "Oferentes de propiedades"

#     price = fields.Float()
#     status = fields.Selection(
#         string="Offer Status",
#         selection=[("accepted", "Accepted"), ("refused", "Refused")],
#         copy=False,
#     )
#     partner_id = fields.Many2one("res.partner", required=True)
#     property_id = fields.Many2one("propiedades", required=True)
#     validity = fields.Integer(default=7)
#     date_deadline = fields.Date(
#         default=lambda self: date_utils.add(fields.Datetime.now(), days=7),
#         compute="_compute_date",
#         inverse="_inverse_date",
#     )

#     @api.depends("validity")
#     def _compute_date(self):
#         for record in self:
#             record.date_deadline = date_utils.add(
#                 fields.Datetime.now(), days=record.validity
#             )

#     @api.depends("date_deadline")
#     def _inverse_date(self):
#         for record in self:
#             print("RECORD VALIDIY", record.validity)
# print("RECORD FECHA", record.date_deadline)


# class Partner(models.Model):
#     _inherit = "res.partner"

#     property_algo = fields.Many2one()
