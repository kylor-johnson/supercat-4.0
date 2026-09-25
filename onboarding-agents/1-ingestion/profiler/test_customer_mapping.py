"""Unit tests for the 2026-09-16 customer-mapping patch.

No iCloud. Price Level vs Price_trade, and propose() latched to the detected
target so a products Name cannot become BillToName.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecat_aliases import PREFIXES, propose
from ecat_vocab import field_in_target, is_ecat_header, patterned_match


class PricePatternTests(unittest.TestCase):
    def test_price_trade_is_product_price_level(self):
        self.assertEqual(
            patterned_match('Price_trade')[0], 'products.csv')
        self.assertTrue(is_ecat_header('Price_trade'))

    def test_price_level_is_not_patterned(self):
        self.assertIsNone(patterned_match('Price Level'))
        self.assertFalse(is_ecat_header('Price Level'))

    def test_stripped_pricetrade_does_not_match(self):
        # Callers must pass a form that still has the underscore.
        self.assertIsNone(patterned_match('pricetrade'))

    def test_price_tempaper_still_matches(self):
        self.assertIsNotNone(patterned_match('Price_tempaper'))


class ProposeTargetTests(unittest.TestCase):
    def _field(self, header, target):
        p = propose(header, target=target)
        return p[0] if p else None

    def _conf(self, header, target):
        p = propose(header, target=target)
        return p[1] if p else None

    def test_name_customers_is_billtoname(self):
        self.assertEqual(self._field('Name', 'customers.csv'), 'BillToName')
        self.assertEqual(self._conf('Name', 'customers.csv'), 'high')

    def test_name_products_is_forbidden(self):
        self.assertIsNone(propose('Name', target='products.csv'))

    def test_company_name_customers(self):
        self.assertEqual(
            self._field('Company Name', 'customers.csv'), 'BillToName')
        self.assertEqual(self._conf('Company Name', 'customers.csv'), 'high')

    def test_company_name_products_is_forbidden(self):
        self.assertIsNone(propose('Company Name', target='products.csv'))

    def test_price_level_customers_is_defaultpricecode(self):
        self.assertEqual(
            self._field('Price Level', 'customers.csv'), 'DefaultPriceCode')
        self.assertEqual(self._conf('Price Level', 'customers.csv'), 'high')

    def test_price_level_products_is_forbidden(self):
        self.assertIsNone(propose('Price Level', target='products.csv'))

    def test_phone_number_and_phone_1(self):
        self.assertEqual(
            self._field('Phone Number', 'customers.csv'), 'BuyerPhone')
        self.assertEqual(self._conf('Phone Number', 'customers.csv'), 'high')
        self.assertEqual(
            self._field('Phone 1', 'customers.csv'), 'BuyerPhone')
        self.assertEqual(self._conf('Phone 1', 'customers.csv'), 'high')
        self.assertEqual(
            self._field('Phone', 'customers.csv'), 'BuyerPhone')

    def test_zip_code_and_street_2(self):
        self.assertEqual(
            self._field('Zip Code', 'customers.csv'), 'BillToPostCode')
        self.assertEqual(
            self._field('Street 2', 'customers.csv'), 'BillToAddress2')

    def test_net_terms_customers_not_netprice(self):
        self.assertEqual(self._field('Net Terms', 'customers.csv'), 'Terms')
        self.assertIsNone(propose('Net Terms', target='products.csv'))

    def test_first_and_last_name_not_longdesc(self):
        self.assertEqual(
            self._field('First & Last Name', 'customers.csv'),
            'BuyerFirstName / BuyerLastName')
        self.assertEqual(
            self._conf('First & Last Name', 'customers.csv'), 'moderate')
        self.assertNotEqual(
            self._field('First & Last Name', 'customers.csv'), 'LongDesc')

    def test_company_is_not_a_prefix(self):
        self.assertIsNone(PREFIXES.match('company name'))

    def test_field_in_target_latch(self):
        self.assertTrue(field_in_target('BillToName', 'customers.csv'))
        self.assertFalse(field_in_target('BillToName', 'products.csv'))
        self.assertTrue(field_in_target('LongDesc', 'products.csv'))
        self.assertFalse(field_in_target('LongDesc', 'customers.csv'))


if __name__ == '__main__':
    unittest.main()
