from odoo import fields, models


class PropiedadesTags(models.Model):
    _name = "propiedades.tagss"
    _description = "Modelo de tags para propiedades"

    name = fields.Char(required=True)
