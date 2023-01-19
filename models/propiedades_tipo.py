from odoo import fields, models


class TipoDePropiedades(models.Model):
    _name = "propiedades.tipo"
    _description = "TIpos de propiedades"

    name = fields.Char(required=True)
