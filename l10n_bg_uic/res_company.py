# -*- encoding: utf-8 -*-
##############################################################################
#
# @author - Rosen Vladimirov, Terraros Commerce <vladimirov.rosen@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import openerp
from openerp import SUPERUSER_ID, tools, api, models
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

CREATE = lambda values: (0, False, values)
UPDATE = lambda id, values: (1, id, values)
DELETE = lambda id: (2, id, False)
FORGET = lambda id: (3, id, False)
LINK_TO = lambda id: (4, id, False)
DELETE_ALL = lambda: (5, False, False)
REPLACE_WITH = lambda ids: (6, False, ids)

class res_company(osv.osv):
	_name = 'res.company'
	_inherit = "res.company"
	_columns = {
		'uic_bg': fields.related('partner_id', 'uic_bg', string=_('UIC'), type="char", size=13, required=True, help=_('UIC by Bulgarian egister agency')),
		'vat_subjected': fields.related('partner_id', 'vat_subjected', string=_('Register by VAT'), type="boolean", help=_('Company is registred by VAT')),
		'vat': fields.related('partner_id', 'vat', string="Tax ID", type="char", size=32),
		'bank_ids': fields.one2many('res.partner.bank','company_id', 'Bank Accounts', help='Bank accounts related to this company'),
	}

#	@api.depends('custom_footer', 'phone', 'fax', 'email', 'website', 'vat', 'company_registry', 'vat_subjected', 'bank_ids')
	@api.v8
	@api.onchange('custom_footer', 'phone', 'fax', 'email', 'website', 'vat', 'company_registry', 'uic_bg', 'vat_subjected', 'bank_ids')
	def uic_change(self):
	    ret = self.env['res.partner']._uic_change('bg', self.uic_bg)
	    if ret:
		return ret

	    cr, uid, context, bank_ids = self.env.cr, self.env.uid, self.env.context, self.bank_ids
	    if self.custom_footer:
		res = self.rml_footer
	    else:
		res = ' | '.join(filter(bool, [
		    self.phone and '%s: %s' % (_('Phone'), self.phone),
		    self.fax and '%s: %s' % (_('Fax'), self.fax),
		    self.email and '%s: %s' % (_('Email'), self.email),
		    self.website and '%s: %s' % (_('Website'), self.website),
		    self.uic_bg and '%s: %s' % (_('UIC'), self.uic_bg),
		    self.vat and '%s: %s' % (_('TIN'), self.vat),
	    	    self.company_registry and '%s: %s' % (_('Reg'), self.company_registry),
	    	    ]))
		_logger.info('print bank_ids: {}'.format(self.bank_ids))
		_logger.info('res + vat + res_vat + bank_ids: %s: %s: %s:' % (res, 'BG' + self.uic_bg, map(REPLACE_WITH, self.bank_ids)))
		# second line: bank accounts
		res_partner_bank = self.pool.get('res.partner.bank')
		#self.registry('res.partner')
#		account_data = self.resolve_2many_commands('bank_ids', self.bank_ids)
#		account_names = res_partner_bank._prepare_name_get(account_data)
#		if account_names:
#		    title = _('Bank Accounts') if len(account_names) > 1 else _('Bank Account')
#		    res += '\n%s: %s' % (title, ', '.join(name for id, name in account_names))

	    if not self.vat_subjected:
		res_vat = ''
		self.vat, self.rml_footer, self.rml_footer_readonly = res_vat, res, res
		super(res_company, self).write({'rml_footer': res, 'rml_footer_readonly': res})
		return {'value': {'vat': res_vat, 'rml_footer': res, 'rml_footer_readonly': res}}

	    if (self.vat_subjected and not self.vat):
		res_vat = 'BG' + self.uic_bg
		self.vat, self.rml_footer, self.rml_footer_readonly = res_vat, res, res
		self.write({'rml_footer': res, 'rml_footer_readonly': res})
		return {'value': {'vat': res_vat, 'rml_footer': res, 'rml_footer_readonly': res}}

	    self.rml_footer, self.rml_footer_readonly = res, res
	    self.write({'rml_footer': res, 'rml_footer_readonly': res})
	    return {'value': {'rml_footer': res, 'rml_footer_readonly': res}}

