from odoo import models, fields, api

class RfidTag(models.Model):
    _name = 'rfid.tag'
    _description = 'RFID Tag'
    
    # Fields definition
    id = fields.Integer(string='ID', required=True)
    epc_code = fields.Char(string='EPC Code', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    last_scan_time = fields.Datetime(string='Last Scan Time')
    last_scan_location = fields.Many2one('stock.location', string='Last Scan Location')
    
    # Add any custom methods or logic here
    @api.model
    def create(self, vals):
        if not vals.get('last_scan_time'):
            vals['last_scan_time'] = fields.Datetime.now()
        return super(RfidTag, self).create(vals)