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
 'author': 'Rosen Vladimirov',
 'description': """
This is the module to manage the Registration Number for Bulgaria in OpenERP
============================================================================
Bulgarian uic by Trade agency. Please first patch base_vat to add support for
check UIC and Bulgarian VAT number.
Copy files base_vat_view.xml.diff and base_vat.py.diff to base directory and
patch it with command patch -p1 < base_vat.py.diff [base_vat_view.xml.diff]
All patch files is found in directory ./patch.
""",
 'website': 'http://www.terarosco.com',
 'name': 'Bulgarian UIC',
 'version': '1.0',
 'category': 'Hidden/Dependency',
 'depends': ['base_vat'],
 'demo': [],
 'data': [
 'res_company_view.xml',
 'res_partner_view.xml',
 ],
 'installable': True,
 'auto_install': False
}
