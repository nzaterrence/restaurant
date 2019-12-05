# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
import pytz

from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class ReportSaleDetailsInclusive(models.AbstractModel):

    _name = 'report.sale_report_inclusive.report_saledetails_inclusive'
    _description = 'Sale Details Inclusive'

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, configs=False):
        """ Serialise the orders of the day information

        params: date_start, date_stop string representing the datetime of order
        """
        if not configs:
            configs = self.env['pos.config'].search([])

        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
        today = today.astimezone(pytz.timezone('UTC'))
        if date_start:
            date_start = fields.Datetime.from_string(date_start)
        else:
            # start by default today 00:00:00
            date_start = today

        if date_stop:
            # set time to 23:59:59
            date_stop = fields.Datetime.from_string(date_stop)
        else:
            # stop by default today 23:59:59
            date_stop = today + timedelta(days=1, seconds=-1)

        # avoid a date_stop smaller than date_start
        date_stop = max(date_stop, date_start)

        date_start = fields.Datetime.to_string(date_start)
        date_stop = fields.Datetime.to_string(date_stop)

        orders = self.env['pos.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_stop),
            ('state', 'in', ['draft','paid','invoiced','done']),
            ('config_id', 'in', configs.ids)])

        draft_orders = orders.filtered(lambda x: x.state == 'draft')

        user_currency = self.env.user.company_id.currency_id

        total = 0.0
        products_sold = {}
        taxes = {}
        for order in orders:
            if user_currency != order.pricelist_id.currency_id:
                total += order.pricelist_id.currency_id._convert(
                    order.amount_total, user_currency, order.company_id, order.date_order or fields.Date.today())
            else:
                total += order.amount_total
            currency = order.session_id.currency_id

            for line in order.lines:
                key = (line.product_id, line.price_unit, line.discount)
                products_sold.setdefault(key, 0.0)
                products_sold[key] += line.qty

                if line.tax_ids_after_fiscal_position:
                    line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1-(line.discount or 0.0)/100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        taxes.setdefault(tax['id'], {'name': tax['name'], 'tax_amount':0.0, 'base_amount':0.0})
                        taxes[tax['id']]['tax_amount'] += tax['amount']
                        taxes[tax['id']]['base_amount'] += tax['base']
                else:
                    taxes.setdefault(0, {'name': _('No Taxes'), 'tax_amount':0.0, 'base_amount':0.0})
                    taxes[0]['base_amount'] += line.price_subtotal_incl

        st_line_ids = self.env["account.bank.statement.line"].search([('pos_statement_id', 'in', orders.ids)]).ids
        if st_line_ids:
            self.env.cr.execute("""
                SELECT aj.name, sum(amount) total
                FROM account_bank_statement_line AS absl,
                     account_bank_statement AS abs,
                     account_journal AS aj 
                WHERE absl.statement_id = abs.id
                    AND abs.journal_id = aj.id 
                    AND absl.id IN %s 
                GROUP BY aj.name
            """, (tuple(st_line_ids),))
            payments = self.env.cr.dictfetchall()
        else:
            payments = []

        # Rooms
        domain = [('checkin', '>=', date_start),
                  ('checkout', '<=', date_stop)]
        reservations = self.env['hotel.reservation'].search(domain)
        unpaid_reservations = reservations.filtered(
            lambda x: x.amount_balance != 0 and x.state == 'confirm')

        return {
            'currency_precision': user_currency.decimal_places,
            'total_paid': user_currency.round(total),
            'payments': payments,
            'company_name': self.env.user.company_id.name,
            'taxes': list(taxes.values()),
            'pos_debts': [{
                'name': l.partner_id.name,
                'amount': l.amount_due
            } for l in draft_orders],
            'room_debts': sorted([{
                'name': l.partner_id.name,
                'reservation_no': l.reservation_no,
                'amount_balance': l.amount_balance
            } for l in unpaid_reservations]),
            'room_total_debts': sum(reservations.mapped('amount_balance')),
            'reservation_total': sum(reservations.mapped('amount_total')),
            'reservation_total_paid': sum(reservations.mapped('amount_total')) - sum(reservations.mapped('amount_balance')),
            'pos_total_debts': sum(draft_orders.mapped('amount_due')),
            'pos_total': sum(orders.mapped('amount_total')) - sum(draft_orders.mapped('amount_due')),
            'reservations': reservations,
            'products': sorted([{
                'product_id': product.id,
                'category': product.pos_categ_id,
                'product_name': product.name,
                'code': product.default_code,
                'quantity': qty,
                'total': qty * price_unit,
                'price_unit': price_unit,
                'discount': discount,
                'uom': product.uom_id.name
            } for (product, price_unit, discount), qty in products_sold.items()], key=lambda l: l['product_name'])
        }

    @api.multi
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        configs = self.env['pos.config'].browse(data['config_ids'])
        data.update(self.get_sale_details(data['date_start'], data['date_stop'], configs))
        return data
