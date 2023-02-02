from odoo import api, fields, models


class TipoDePropiedades(models.Model):
    _name = "propiedades.tipo"
    _description = "Tipos de propiedades"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("propiedades", "property_type")
    offer_ids = fields.One2many("propiedades.oferentes", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    sequence = fields.Integer("Sequence")
    color = fields.Integer()

    @api.depends("offer_ids")  # pendiente añadir el counteo
    def _compute_offer_count(self):
        for record in self:
            pass

    def propiedades_view_types_offer(self):
        pass

    _sql_constraints = [
        (
            "unique_name",
            "unique(name)",
            "House type name must be unique. There is already a type with that name",
        )
    ]
