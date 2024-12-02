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

class LaporanPenjualanWizard(models.TransientModel):
    _name = "laporan.penjualan.wizard"
    _description = "Laporan Penjualan Wizard"


    today = (fields.Datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=1)) - timedelta(hours=7)
    end = today - timedelta(seconds=1)

    date_from = fields.Datetime(string='Start Date', required=True, default=start_date_default())
    date_to = fields.Datetime(string='End Date', required=True, default=end)
    type = fields.Selection([('service', 'Service'), ('retail', 'Retail'), ('all', 'All')], required=True, index=True)
    employee = fields.Many2many('res.partner', string='Employee', required=False, domain=['|', ('is_employee', '=', 1), ('is_capster', '=', 1)])
    all_employee = fields.Boolean(string="All Employee", default=False, )


    def action_print_kartu(self):
        emp = ""
        data_penjualan = []
        if self.all_employee:
            emp = "All"
            if self.type == 'all':
                for line in self.env['pos.order.line'].search([('order_id.date_order', '>=', self.date_from), ('order_id.date_order', '<=', self.date_to)], order="capster_id"):
                    data_penjualan.append([
                        str(line.order_id.date_order).split(' ')[0],
                        line.capster_id.name,
                        line.product_id.type,
                        line.product_id.categ_id.name,
                        line.product_id.name,
                        line.product_id.name,
                        line.order_id.partner_id.name,
                        line.qty,
                        line.product_uom_id.name,
                        round(line.price_subtotal_incl / 1.11),
                        line.price_subtotal_incl
                    ])
            if self.type == 'service':
                for line in self.env['pos.order.line'].search(
                        [('order_id.date_order', '>=', self.date_from), ('order_id.date_order', '<=', self.date_to), ('product_id.type', '=', 'service')],
                        order="capster_id"):
                    data_penjualan.append([
                        str(line.order_id.date_order).split(' ')[0],
                        line.capster_id.name,
                        line.product_id.type,
                        line.product_id.categ_id.name,
                        line.product_id.name,
                        line.product_id.name,
                        line.order_id.partner_id.name,
                        line.qty,
                        line.product_uom_id.name,
                        round(line.price_subtotal_incl / 1.11),
                        line.price_subtotal_incl
                    ])
            if self.type == 'retail':
                for line in self.env['pos.order.line'].search(
                        [('order_id.date_order', '>=', self.date_from), ('order_id.date_order', '<=', self.date_to),
                         ('product_id.type', '=', 'product')],
                        order="capster_id"):
                    data_penjualan.append([
                        str(line.order_id.date_order).split(' ')[0],
                        line.capster_id.name,
                        line.product_id.type,
                        line.product_id.categ_id.name,
                        line.product_id.name,
                        line.product_id.name,
                        line.order_id.partner_id.name,
                        line.qty,
                        line.product_uom_id.name,
                        round(line.price_subtotal_incl / 1.11),
                        line.price_subtotal_incl
                    ])
        else:
            emp = self.employee.mapped('name')
            if self.type == 'all':
                for line in self.env['pos.order.line'].search(
                        [('order_id.date_order', '>=', self.date_from), ('order_id.date_order', '<=', self.date_to), ('capster_id', 'in', self.employee.mapped('id'))],
                        order="capster_id"):
                    data_penjualan.append([
                        str(line.order_id.date_order).split(' ')[0],
                        line.capster_id.name,
                        line.product_id.type,
                        line.product_id.categ_id.name,
                        line.product_id.name,
                        line.product_id.name,
                        line.order_id.partner_id.name,
                        line.qty,
                        line.product_uom_id.name,
                        round(line.price_subtotal_incl / 1.11),
                        line.price_subtotal_incl
                    ])
            if self.type == 'service':
                for line in self.env['pos.order.line'].search(
                        [('order_id.date_order', '>=', self.date_from), ('order_id.date_order', '<=', self.date_to),
                         ('product_id.type', '=', 'service'), ('capster_id', 'in', self.employee.mapped('id'))],
                        order="capster_id"):
                    data_penjualan.append([
                        str(line.order_id.date_order).split(' ')[0],
                        line.capster_id.name,
                        line.product_id.type,
                        line.product_id.categ_id.name,
                        line.product_id.name,
                        line.product_id.name,
                        line.order_id.partner_id.name,
                        line.qty,
                        line.product_uom_id.name,
                        round(line.price_subtotal_incl / 1.11),
                        line.price_subtotal_incl
                    ])
            if self.type == 'retail':
                for line in self.env['pos.order.line'].search(
                        [('order_id.date_order', '>=', self.date_from), ('order_id.date_order', '<=', self.date_to),
                         ('product_id.type', '=', 'product'), ('capster_id', 'in', self.employee.mapped('id'))],
                        order="capster_id"):
                    data_penjualan.append([
                        str(line.order_id.date_order).split(' ')[0],
                        line.capster_id.name,
                        line.product_id.type,
                        line.product_id.categ_id.name,
                        line.product_id.name,
                        line.product_id.name,
                        line.order_id.partner_id.name,
                        line.qty,
                        line.product_uom_id.name,
                        round(line.price_subtotal_incl / 1.11),
                        line.price_subtotal_incl
                    ])
        print(data_penjualan)
        data = {
            'start': str(self.date_from + timedelta(hours=7)).split(" ")[0],
            'end': str(self.date_to + timedelta(hours=7)).split(" ")[0],
            'type': self.type,
            'emp': str(emp).replace("\'", ""),
            'data_penjualan': data_penjualan
        }

        return self.env.ref('accounting_excel_report.report_laporan_penjualan_xlsx').report_action(self, data=data)
