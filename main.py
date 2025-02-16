import os
from datetime import datetime
from decimal import Decimal
from typing import List
import json

from services.reconciler.implementations.reconciler import DefaultReconEngine
from services.common.models.payment import Payment

def setup_environment():
    """
    Set up environment variables if not already set.
    In production, these should be set in the environment or .env file.
    """
    if not os.getenv("MONGO_URI"):
        # For testing, use a local MongoDB instance
        os.environ["MONGO_URI"] = "mongodb://localhost:27017"
    
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable must be set")

def create_payment_advice_file():
    """Create a sample payment advice file if it doesn't exist."""
    advice_path = "C:/Users/abcom/Documents/recon-agent/metadata/payment_advices.json"
    if not os.path.exists(advice_path):
        sample_data = [
            {
                "payment_date": "01-04-2024",
                "total_amount": 1000.00,
                "invoice_number": "INV001"
            }
        ]
        with open(advice_path, 'w') as f:
            json.dump(sample_data, f, indent=4)

def load_sample_payments() -> List[Payment]:
    """
    Create sample payments for testing.
    In a real scenario, you would load these from a database or file.
    """
    return [
        Payment(
            transaction_id= "ICIC0000105",
            transaction_date= "29-01-2025",
            payer= "DARSHITA SOUTHERN",
            direction= "credit",
            payment_mode= "NEFT",
            category= "transfer_in",
            amount= Decimal("20532.0"),
            balance_impact= Decimal("20532.0"),
            bank_name= "ICICI Bank"
        )
    ]

def main():
    print("🚀 Starting reconciliation process...")
    
    try:
        # Set up environment
        setup_environment()
        print("✅ Environment configured")
        
        # Create payment advice file if needed
        create_payment_advice_file()
        print("✅ Payment advice file checked")
        
        # Initialize the reconciliation engine
        recon_engine = DefaultReconEngine()
        print("✅ Reconciliation engine initialized successfully")
        
        # Load payments
        payments = load_sample_payments()
        print(f"📥 Loaded {len(payments)} payments for processing")

        # Process each payment
        for payment in payments:
            print(f"\n🔄 Processing payment {payment.transaction_id}")
            print(f"   Amount: ₹{payment.amount:,.2f}")
            print(f"   Payer: {payment.payer}")
            print(f"   Date: {payment.transaction_date}")
            
            try:
                matched_invoices = recon_engine.reconcile(payment)
                
                if matched_invoices:
                    print(f"\n✅ Found {len(matched_invoices)} matching invoices:")
                    for invoice in matched_invoices:
                        print("\n🔍 Invoice Details:")
                        print(f"   Invoice Number: {invoice.invoice_no}")
                        print(f"   Date: {invoice.invoice_date}")
                        print(f"   Party Name: {invoice.party_name}")
                        print(f"   GSTIN: {invoice.gstin}")
                        print(f"   Type: {invoice.type}")
                        print(f"   Unit: {invoice.unit}")
                        print(f"   Branch: {invoice.branch}")
                        
                        print("\n   Amount Details:")
                        print(f"   - Basic Amount: ₹{invoice.basic_amount:,.2f}")
                        print(f"   - CGST: ₹{invoice.cgst:,.2f}")
                        print(f"   - SGST: ₹{invoice.sgst:,.2f}")
                        print(f"   - IGST: ₹{invoice.igst:,.2f}")
                        if hasattr(invoice, 'tcs'):
                            print(f"   - TCS: ₹{invoice.tcs:,.2f}")
                        if hasattr(invoice, 'freight'):
                            print(f"   - Freight: ₹{invoice.freight:,.2f}")
                        if hasattr(invoice, 'pkg_fwd'):
                            print(f"   - Packaging & Forwarding: ₹{invoice.pkg_fwd:,.2f}")
                        if hasattr(invoice, 'rounding'):
                            print(f"   - Rounding: ₹{invoice.rounding:,.2f}")
                        print(f"   - Total Amount: ₹{invoice.total:,.2f}")
                        print("   ----------------------------------------")
                else:
                    print("❌ No matching invoices found")
                    
            except Exception as e:
                print(f"❌ Error processing payment: {str(e)}")
                
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return

if __name__ == "__main__":
    main() 