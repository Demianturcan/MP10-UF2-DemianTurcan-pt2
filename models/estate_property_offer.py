# filepath: /home/alumne/Code/mp10-uf2-odoo/odoo-dev/addons/estate/models/estate_property_offer.py
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('Preu de l’Oferta', required=True)
    status = fields.Selection([
        ('accepted', 'Acceptada'),
        ('refused', 'Rebutjada'),
        ('pending', 'En tractament'),
    ], string='Estat', default='pending')
    partner_id = fields.Many2one(
        'res.partner', string='Comprador', required=True)
    property_id = fields.Many2one(
        'estate.property', string='Propietat', required=True)
    comments = fields.Text('Comentaris')


#mètode per actualitzar la propietat quan una oferta és acceptada
    def _update_property_on_acceptance(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.write({
                    'buyer_id': offer.partner_id.id,  
                    'final_selling_price': offer.price, 
                })

#sobreescrivim el mètode create per actualitzar la propietat quan es crea una oferta acceptada
    @api.model
    def create(self, vals_list):
        record = super(EstatePropertyOffer, self).create(vals_list)
        if vals_list.get('status') == 'accepted':
            record._update_property_on_acceptance()
        return record

#sobreescrivim el mètode write per actualitzar la propietat quan es canvia l'estat a acceptat
    def write(self, vals):
        res = super(EstatePropertyOffer, self).write(vals)
        if 'status' in vals and vals['status'] == 'accepted':
            self._update_property_on_acceptance()
        return res