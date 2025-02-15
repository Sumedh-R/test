class Config:
    # Database configurations
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "myapp"
    
    # Payment configurations
    STRIPE_API_KEY = "your_stripe_key"
    RAZORPAY_KEY = "your_razorpay_key"
    
    # Notification configurations
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SMS_API_KEY = "your_sms_api_key" 