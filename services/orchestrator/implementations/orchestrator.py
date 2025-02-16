from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv
from services.orchestrator.orch_interface import OrchInterface

load_dotenv()

class Orchestrator(OrchInterface):
    def perform_recon(self, customer = None):
        MONGO_URI = os.getenv('MONGO_URI')

        try:
            client = MongoClient(MONGO_URI)

            db = client.get_database("Lumens")

            payment_collection = db["bank_details"]
            payment_data = list(payment_collection.find())

            return payment_data
        
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
# if __name__ == "__main__":
#     fetcher = Mongofetcher()
#     invoice_data, payment_data = fetcher.fetch_data()

#     print(len(invoice_data), len(payment_data))
