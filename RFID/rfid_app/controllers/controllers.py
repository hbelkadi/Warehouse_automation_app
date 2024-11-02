# -*- coding: utf-8 -*-
# from odoo import http


# class RfidApp(http.Controller):
#     @http.route('/rfid_app/rfid_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rfid_app/rfid_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rfid_app.listing', {
#             'root': '/rfid_app/rfid_app',
#             'objects': http.request.env['rfid_app.rfid_app'].search([]),
#         })

#     @http.route('/rfid_app/rfid_app/objects/<model("rfid_app.rfid_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rfid_app.object', {
#             'object': obj
#         })
