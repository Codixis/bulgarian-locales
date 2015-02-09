# -*- encoding: utf-8 -*-
##############################################################################
#
# @author - Rosen Vladimirov <vladimirov.rosen@gmail.com>
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
{
"name" : "Bulgaria - Accounting",
"version" : "1.0",
"author" : "Rosen Vladimirov",
"website": "http://www.terarosco.com",
"category" : "Localization/Account Charts",
"depends" : ['account','account_chart','base_vat'],
"description": """
This is the module to manage the Accounting Chart, VAT structure, Fiscal Position and Tax Mapping.
It also adds the Registration Number for Bulgaria in OpenERP.
================================================================================================================
Romanian accounting chart and localization.
""",
"demo" : [],
"data" : [
'account_chart.xml',
'account_tax_code_template.xml',
'account_chart_template.xml',
'account_tax_template.xml',
'fiscal_position_template.xml',
'l10n_chart_bg_wizard.xml',
],
"installable": True,
}
