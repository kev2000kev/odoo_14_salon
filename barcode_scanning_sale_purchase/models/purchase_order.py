from odoo import api, models, fields


class PurchaseOrderLines(models.Model):
    _inherit = "purchase.order.line"

    barcode_scan = fields.Char(string='Product Barcode', help="Here you can provide the barcode for the product")

    @api.onchange('barcode_scan')
    def _onchange_barcode_scan(self):
        product_rec = self.env['product.product']
        if self.barcode_scan:
            product = product_rec.search([('product_multi_barcodes.multi_barcode', '=', self.barcode_scan)])
            self.product_id = product.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super(PurchaseOrderInherit, self).button_confirm()

        print("000000000000000000000\n\n\n\n\n\n\n\n\n\n\n\n")
        for picking in self.env['stock.picking'].search([('origin', '=', self.name)]):
            for line in picking.move_line_ids_without_package:
                line.write({
                    'qty_done': line.product_uom_qty
                })
            print(picking.name)
            picking.action_confirm()
            picking.action_assign()
            picking.with_context(default_immediate_transfer=False).button_validate()

        return res