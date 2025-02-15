import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime
from services.reconciliation.implementations.script_recon import ScriptRecon

class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.sample_payment = {
            "transaction_id": "TEST123",
            "transaction_date": "13-01-2025",
            "payer": "TEST COMPANY",
            "direction": "credit",
            "payment_mode": "NEFT",
            "amount": 10000.0,
            "balance_impact": 10000.0,
            "bank_name": "Test Bank"
        }
        
        self.sample_invoices = [
            {
                "Invoice No": "INV001",
                "Date": "10-01-2025",
                "Party": "TEST COMPANY",
                "Total": "10000.00"
            }
        ]

        self.recon = ScriptRecon()

    def test_normalize_date(self):
        test_cases = [
            ("02-01-24", "02-01-2024"),
            ("01-08-2024", "01-08-2024"),
            ("03-Dec-24", "03-12-2024"),
            ("07-Jan-2025", "07-01-2025")
        ]
        
        for input_date, expected in test_cases:
            with self.subTest(input_date=input_date):
                result = self.recon.normalize_date(input_date)
                self.assertEqual(result, expected)

    @patch('services.reconciliation.implementations.script_recon.ScriptRecon')
    def test_llm_namescore(self, mock_llm):
        mock_response = Mock()
        mock_response.content = json.dumps([self.sample_invoices[0]])
        
        mock_chain = Mock()
        mock_chain.invoke.return_value = mock_response
        
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.__or__.return_value = mock_chain

        self.recon.llm = mock_llm_instance
        
        result = self.recon.llm_matcher(self.sample_payment, self.sample_invoices)

        self.assertEqual(json.loads(result), [self.sample_invoices[0]])

    @patch('services.reconciliation.implementations.script_recon.ScriptRecon')
    def test_refiner(self, mock_llm):
        mock_response = Mock()
        mock_response.content = "1"
        
        mock_chain = Mock()
        mock_chain.invoke.return_value = mock_response
        
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.__or__.return_value = mock_chain
        
        result = self.recon.refiner(self.sample_payment["payer"], json.dumps(self.sample_invoices[0]))
        self.assertEqual(result, 1) 