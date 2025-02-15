import unittest
from services.payments.implementations.stripe_payment import StripePayment
from services.payments.implementations.razorpay_payment import RazorpayPayment

class TestPayments(unittest.TestCase):
    def setUp(self):
        self.stripe = StripePayment()
        self.razorpay = RazorpayPayment()

    def test_stripe_payment(self):
        self.assertTrue(self.stripe.process_payment(100.0, "USD"))

    def test_razorpay_payment(self):
        self.assertTrue(self.razorpay.process_payment(100.0, "INR")) 