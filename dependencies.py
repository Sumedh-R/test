from dependency_injector import containers, providers
from services.payments.implementations.stripe_payment import StripePayment
from services.payments.implementations.razorpay_payment import RazorpayPayment
from services.users.implementations.sql_user_repository import SQLUserRepository
from services.users.implementations.mongo_user_repository import MongoUserRepository
from services.notifications.implementations.email_notification import EmailNotification
from services.notifications.implementations.sms_notification import SMSNotification

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Payment services
    stripe_payment = providers.Singleton(StripePayment)
    razorpay_payment = providers.Singleton(RazorpayPayment)
    
    # User repositories
    sql_user_repository = providers.Singleton(SQLUserRepository)
    mongo_user_repository = providers.Singleton(MongoUserRepository)
    
    # Notification services
    email_notification = providers.Singleton(EmailNotification)
    sms_notification = providers.Singleton(SMSNotification) 