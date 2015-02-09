# -*- encoding: utf-8 -*-
##############################################################################
#
# Romanian accounting localization for OpenERP V7
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
from openerp import tools, api, models
from openerp.osv import osv, fields
from openerp.tools.translate import _
import uuid
import logging

_logger = logging.getLogger(__name__)

class res_partner(osv.osv):
	_name = 'res.partner'
	_inherit = "res.partner"
	_columns = {
		'vat': fields.char('TIN', help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements."),
		'uic_bg': fields.char(string=_('UIC'), size=13, required=True, help=_('UIC by Bulgarian egister agency')),
		'is_company': fields.boolean('Is a Company', help="Check if the contact is a company, otherwise it is a person"),
		'vat_subjected': fields.boolean('VAT Legal Statement', help="Check this box if the partner is subjected to the VAT. It will be used for the VAT legal statement."),
	}

	_defaults = {
	    'uic_bg': api.model(lambda self: ('self_' + str(uuid.uuid1().time)) ),
	}

	_sql_constraints = [
		('uic_bg_uniq', 'unique (uic_bg)', 'The company register number must be unique !')
	]

	@api.model
    	def _uic_change(self, country_code, uic_bg):
	    if not (self.simple_vat_check(country_code, uic_bg)):
		    return {
			    'warning': {
		            'title': _("Bulgarian Unicue indetifation code"),
            	            'message': _("Bulgarian Unique identification code %s is not correct, please check code again.") % (uic_bg),
	        	    }
    			   }
            return {}

#	@api.depends('is_company', 'vat')
	@api.v8
	@api.onchange('is_company')
	def uic_type_change(self):
	    ret = self.onchange_type(self.is_company)
	    if not self.is_company:
		self.uic_bg = ('self_' + str(uuid.uuid1().time))
		self.vat = ''
	    if (self.is_company and ('self_' in self.uic_bg)):
		self.uic_bg = ''
		self.vat = ''
	    ret['value'].update({'vat': self.vat, 'uic_bg': self.uic_bg})
#	    _logger.info('is vat, uic_bg, vat_subjected, is_company: %s: %s: %s: %s:' % (self.vat, 'BG' + self.uic_bg, self.vat_subjected, is_company))
	    return ret

#	@api.depends('vat', 'vat_subjected', 'is_company')
	@api.v8
	@api.onchange('uic_bg', 'vat', 'vat_subjected')
	def uic_change(self):
	    if not self.is_company:
		return {}
	    ret = self._uic_change('bg', self.uic_bg)
	    if not ret:
    	        if not self.vat_subjected:
		    self.vat = ''
		    ret = {'value': {'vat': ''}}
    	    if (self.vat_subjected and not self.vat):
		self.vat = 'BG' + self.uic_bg
		ret = {'value': {'vat': 'BG' + self.uic_bg}}
	    _logger.info('uic vat, uic_bg, vat_subjected, is_company: %s: %s: %s: %s:' % (self.vat, 'BG' + self.uic_bg, self.vat_subjected, self.is_company))
	    return ret

 	def _commercial_fields(self, cr, uid, context=None):
            return super(res_partner, self)._commercial_fields(cr, uid, context=context) + ['uic_bg']

