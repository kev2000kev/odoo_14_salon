# -*- coding: utf-8 -*-

from odoo import models
from datetime import date, datetime

def date_to_tanggal(st):
    date_split = st.split("-")
    bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober',
             'November', 'Desember']
    return date_split[2] + " " + bulan[int(date_split[1]) - 1] + " " + date_split[0]
class SummaryPejualanXlsx(models.AbstractModel):
    _name = 'report.accounting_excel_report.report_summary_penjualan_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, stock):
        today = date.today()
        dt = 'Tanggal Print : ' + str(today.strftime("%Y-%m-%d"))
        bold = workbook.add_format({'bold': True, 'border': 1})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'border': 1,'bg_color': '#cccccc'})
        title = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
        format_data = workbook.add_format({'border': 1})
        heading1 = workbook.add_format({'bold': True, 'border': 1, 'align': 'left', 'font_size': 18})
        heading2 = workbook.add_format({'bold': True, 'align': 'center', 'border': 0, 'font_size': 14})
        heading3 = workbook.add_format({'bold': False, 'align': 'center', 'border': 0, 'font_size': 12})


        sheet = workbook.add_worksheet('Summary Penjualan')
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 50)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        sheet.set_column('K:K', 20)
        sheet.set_column('L:L', 20)

        sheet.merge_range(0, 0, 0, 9, 'THE PARLOUR HAIRDRESSING', heading1)
        sheet.merge_range(1, 0, 1, 9, 'Laporan Summary Penjualan', heading2)
        sheet.merge_range(2, 0, 2, 9, 'Periode : ' + date_to_tanggal(str(data['start'])) + ' - ' + date_to_tanggal(str(data['end'])), heading3)
        sheet.merge_range(3, 0, 3, 9, 'type : ' + str(data['type']), heading3)
        sheet.merge_range(4, 0, 4, 9, 'Employee : ' + str(data['emp']), heading3)


        sheet.write(6, 0, 'Date', title)
        sheet.write(6, 1, 'Nama', title)
        sheet.write(6, 2, 'Tipe', title)
        sheet.write(6, 3, 'Category', title)
        sheet.write(6, 4, 'Service / Product Name', title)
        sheet.write(6, 5, 'Desc', title)
        sheet.write(6, 6, 'Qty', title)
        sheet.write(6, 7, 'UOM', title)
        sheet.write(6, 8, 'DPP', title)
        sheet.write(6, 9, 'Amount', title)

        row = 6
        for i in data['data_penjualan']:
            row += 1
            sheet.write(row, 0, i[0], format_data)
            sheet.write(row, 1, i[1], format_data)
            sheet.write(row, 2, i[2], format_data)
            sheet.write(row, 3, i[3], format_data)
            sheet.write(row, 4, i[4], format_data)
            sheet.write(row, 5, i[5], format_data)
            sheet.write(row, 6, i[6], format_data)
            sheet.write(row, 7, i[7], format_data)
            sheet.write(row, 8, i[8], format_data)
            sheet.write(row, 9, i[9], format_data)

























