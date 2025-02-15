import json
import os
import faiss
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from services.reconciliation.recon_interface import ReconInterface
from services.orchestrator.implementations.sample_reader import Mongofetcher
import re

load_dotenv()

class ScriptRecon(ReconInterface):
    def __init__(self):
        self.llm = None
        self.payment_advdata = None
        self.paymentadvpath = 'C:/Users/abcom/Documents/Recon-agent/payment_advices.json'

    def init_llm(self):
        api_key = os.getenv("OPENAI_API_KEY")

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
        )

    def normalize_date(self, date_str):
        formats = [
            "%d-%m-%y",
            "%d-%m-%Y",
            "%d-%b-%y",
            "%d-%b-%Y",
            "%d-%B-%y",
            "%d-%B-%Y"
        ]
        
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime("%d-%m-%Y")
            except ValueError:
                continue
        
        raise ValueError(f"Unsupported date format: {date_str}")
    
    def convert_json(self, raw_json):
        # Replace ObjectId("...") with just "..."
        cleaned_json = re.sub(r'ObjectId\("([a-f0-9]+)"\)', r'"\1"', raw_json)
        return json.loads(cleaned_json)
        
    def llm_matcher(self, payment, invoices):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                     "system",
                    "You are a helpful assistant that is able to match payments to invoices. You have a payment: {payment} at hand \
                    and a list of invoice jsons {invoices}. You will map payments to invoices. Some of the points you must take into consideration while mapping are:\
                    1. The transaction date when the payment was made will always be greater than or equal to the date of issuing the invoice.\
                    2. The payer name in the payment and the party name in the invoice should refer to the same company. There might be slight differences\
                    All the above conditions are compulsory for a map.\
                    You can also make additional reasonings of your own\
                    You will remove invoices that do not satisfy this criterion\
                    Do not modify the data to suit your purpose\
                    You will return a list of jsons containing the invoices that map to the payment. \
                    You will not return any other extra text\
                    You have vast experience in this domain and can hence clearly perform this task with great attention to detail.",
                ),
            ]
        )

        chain = prompt | self.llm
        message = chain.invoke(
            {
                "payment": payment,
                "invoices": invoices,
            }
        )

        return message.content
    
    def refiner(self, payments, invoices):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                     "system",
                    "You are a helpful assistant that is able to refine representation based on some conditions. You are given\
                    a {payments} and an item {invoices}. You will verify the foll conditions:\
                    1. The transaction date field in {payments} will always be greater than or equal to the date field (if exists) in the {invoices}.\
                    2. The amount field in {payments} will always be lesser than or equal to the Total amount field(if exists) in {invoices} with slight variation around 2-3%\
                    3. The payer name field in the {payments} and the party name field(if exists) in the {invoices} refer to the same company. There might be slight differences\
                    You can clearly make this distinction.\
                    You will return 1 if the all of the above conditions satisfy else you return 0. You will not return any other text"
                ),
            ]
        )

        chain = prompt | self.llm
        message = chain.invoke(
            {
                "payments": payments,
                "invoices": invoices,
            }
        )

        return int(message.content)
    
    def reconcile(self, invoice_data, payment_data):
        with open(self.paymentadvpath, 'r') as f:
            self.payment_advdata = json.load(f)
        
        self.init_llm()

        credit_payments = [payment for payment in payment_data if payment['direction'] == "credit"]

        target_payment = {
        "transaction_id": "ICIC0000105",
        "transaction_date": "29-01-2025",
        "payer": "DARSHITA SOUTHERN",
        "direction": "credit",
        "payment_mode": "NEFT",
        "category": "transfer_in",
        "amount": 20532.0,
        "balance_impact": 20532.0,
        "bank_name": "ICICI Bank"
    }

        payment_date = self.normalize_date(target_payment['transaction_date'])

        target_paymentadvs = []

        for payment_adv in self.payment_advdata:
            paymentadv_date = self.normalize_date(payment_adv['payment_date'])
            if target_payment['amount'] == payment_adv['total_amount'] and payment_date == paymentadv_date:
                target_paymentadvs.append(payment_adv)

        if len(target_paymentadvs) != 0:
            all_invoices = []
            target_invoices = []
            for item in target_paymentadvs:
                invoicenum = item['invoice_number']
                target_invoices = [invoice for invoice in invoice_data if invoice['Invoice No'] == invoicenum]
                all_invoices.extend(target_invoices)

            print("With payment advice")
            print(json.dumps(all_invoices, indent = 4))

        else:
            new_invoices = []
            for invoice in invoice_data:
                if float(invoice["Total"]) >= target_payment["amount"]:
                    new_invoices.append(invoice)

            print("Without payment advice")

            responses_list = []

            for i in range(0, len(new_invoices), 50):
                target_invoices = new_invoices[i:i+50]
                response = self.llm_matcher(target_payment, target_invoices)
                responses_list.append(response)

            print(responses_list)

            print("Printing refined responses\n")
            for response in responses_list:
                answer = self.refiner(target_payment["payer"], response)

                if answer == 1:
                    print(response)

# if __name__ == "__main__":
#     recon = ScriptRecon()
#     recon.reconcile()