import unittest
from unittest.mock import patch, Mock
from services.orchestrator.implementations.sample_reader import Mongofetcher

class TestMongofetcher(unittest.TestCase):
    @patch('services.orchestrator.implementations.sample_reader.MongoClient')
    def test_fetch_data(self, mock_mongo_client):
        # Setup mock data
        mock_invoice_data = [{"invoice_id": "1"}]
        mock_payment_data = [{"payment_id": "1"}]
        
        # Configure mock MongoDB responses
        mock_db = Mock()
        mock_collection_invoices = Mock()
        mock_collection_payments = Mock()
        
        mock_collection_invoices.find.return_value = mock_invoice_data
        mock_collection_payments.find.return_value = mock_payment_data
        
        mock_db.invoices = mock_collection_invoices
        mock_db.payments = mock_collection_payments
        
        mock_client = Mock()
        mock_client.__getitem__.return_value = mock_db
        mock_mongo_client.return_value = mock_client
        
        # Test the fetcher
        fetcher = Mongofetcher()
        invoices, payments = fetcher.fetch_data()
        
        # Verify results
        self.assertEqual(invoices, mock_invoice_data)
        self.assertEqual(payments, mock_payment_data) 