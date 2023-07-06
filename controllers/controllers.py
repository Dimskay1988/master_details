# -*- coding: utf-8 -*-
# from odoo import http


# class MasterDetails(http.Controller):
#     @http.route('/master_details/master_details', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/master_details/master_details/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('master_details.listing', {
#             'root': '/master_details/master_details',
#             'objects': http.request.env['master_details.master_details'].search([]),
#         })

#     @http.route('/master_details/master_details/objects/<model("master_details.master_details"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('master_details.object', {
#             'object': obj
#         })
