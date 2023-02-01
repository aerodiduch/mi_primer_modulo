from odoo import fields, models


class TipoDePropiedades(models.Model):
    _name = "propiedades.tipo"
    _description = "TIpos de propiedades"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("propiedades", "property_type")
    sequence = fields.Integer("Sequence")
    color = fields.Integer()

    _sql_constraints = [
        (
            "unique_name",
            "unique(name)",
            "House type name must be unique. There is already a type with that name",
        )
    ]
