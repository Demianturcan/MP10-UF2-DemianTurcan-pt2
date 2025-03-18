from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Propietat Immobiliària',
                       required=True, default='Nova Propietat')
    description = fields.Text('Descripció de la Propietat',
                              copy=False, default='Descripció per defecte')
    date_availability = fields.Date('Data de Disponibilitat', default=lambda self: date.today(
    ) + relativedelta(months=1), copy=False)
    selling_price = fields.Float('Preu de venda esperat', required=True, default=150000.0)
    final_selling_price = fields.Float(
        'Preu de venda final', readonly=True, copy=False)
    best_offer = fields.Float(
        'Millor oferta', compute='_compute_best_offer', readonly=True, store=False)
    postalcode = fields.Char('Codi postal', default='08001')
    bedrooms = fields.Integer('Habitacions', default=3)
    state = fields.Selection([
        ('new', 'Nova'),
        ('offer_received', 'Oferta Rebuda'),
        ('offer_accepted', 'Oferta Acceptada'),
        ('sold', 'Venuda'),
        ('canceled', 'Cancel·lada'),
    ], string='Estat de l’Anunci', default='new')
    active = fields.Boolean('Actiu', default=True)
    elevator = fields.Boolean('Ascensor', default=False)
    parking = fields.Boolean('Aparcament', default=True)
    renovated = fields.Boolean('Renovat', default=True)
    bathrooms = fields.Integer('Banys', default=2)
    area = fields.Integer('Superfície', required=True, default=100)
    price_per_sqm = fields.Float(
        'Preu per m2', compute='_compute_price_per_sqm', readonly=True)
    year_built = fields.Integer('Any de construcció', default=2000)
    energy_certificate = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
    ], string='Certificat Energètic', default='C')
    buyer_id = fields.Many2one('res.partner', string='Comprador', readonly=True)
    salesperson_id = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user)
    property_type_id = fields.Many2one('estate.property.type', string='Tipus de Propietat')
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Ofertes')

    @api.depends('selling_price', 'area')
    def _compute_price_per_sqm(self):
        for record in self:
            if record.area > 0:
                record.price_per_sqm = record.selling_price / record.area
            else:
                record.price_per_sqm = 0

    @api.depends('offer_ids.price', 'offer_ids.status')
    def _compute_best_offer(self):
        for record in self:
            valid_offers = record.offer_ids.filtered(lambda o: o.status != 'refused')
            if valid_offers:
                record.best_offer = max(valid_offers.mapped('price'))
            else:
                record.best_offer = 0.0