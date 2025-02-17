from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name=fields.Char('Nom', required=True)