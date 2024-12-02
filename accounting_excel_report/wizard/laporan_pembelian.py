# -*- coding: utf-8 -*-
from ftplib import all_errors

from odoo import api, fields, models
from datetime import timedelta, date
import dateutil.parser
from datetime import timedelta, date
import dateutil.parser
import datetime
from dateutil.relativedelta import relativedelta

def rpformat(nominal):
    def formatrupiah(uang):
        y = str(uang)
        if len(y) <= 3:
            return y
        else:
            p = y[-3:]
            q = y[:-3]
            return formatrupiah(q) + '' + p

    nominal = int(nominal)
    return formatrupiah(nominal)

def start_date_default():
    today = fields.Datetime.now()
    return today.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=7)

class LaporanPembelianWizard(models.TransientModel):
    _name = "laporan.pembelian.wizard"
    _description = "Laporan Pembelian Wizard"


    today = (fields.Datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=1)) - timedelta(hours=7)
    end = today - timedelta(seconds=1)

    date_from = fields.Datetime(string='Start Date', required=True, default=start_date_default())
    date_to = fields.Datetime(string='End Date', required=True, default=end)


    def action_print_kartu(self):

        data_pembelian = []
        for bill in self.env['account.move'].search([('move_type', '=', 'in_invoice'), ('invoice_date', '>=', self.date_from), ('invoice_date', '<=', self.date_to), ('state', '=', 'posted')]):
            for line in bill.invoice_line_ids:
                data_pembelian.append([
                    line.move_id.invoice_origin,
                    line.move_id.invoice_date,
                    line.move_id.partner_id.name,
                    line.product_id.categ_id.name,
                    line.product_id.name,
                    line.product_id.name,
                    line.quantity,
                    line.product_uom_id.name,
                    line.price_unit,
                    line.price_subtotal
                ])

        data = {
            'start': str(self.date_from + timedelta(hours=7)).split(" ")[0],
            'end': str(self.date_to + timedelta(hours=7)).split(" ")[0],
            'data_pembelian': data_pembelian
        }

        return self.env.ref('accounting_excel_report.report_laporan_pembelian_xlsx').report_action(self, data=data)
