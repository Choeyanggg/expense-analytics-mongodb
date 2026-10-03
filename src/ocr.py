from google import genai
from dotenv import load_dotenv
load_dotenv()
import os

api_key=os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)

def extract_transaction(image_path):
    with open(image_path,"rb") as f:
        image_data=f.read()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            {"text":"""
            Analyze this expense receipt.

            Extract the transaction information and return ONLY valid JSON
            with exactly these fields:

            {
                "date": "YYYY-MM-DD",
                "mode": "string",
                "category": "string",
                "subcategory": "string or null",
                "note": "string or null",
                "amount": number,
                "income_expense": "Income or Expense",
                "currency": "INR"
            }

            Rules:
            - date: use the transaction/receipt date.
            - mode: payment method such as Cash, UPI, Credit Card, Debit Card.
            - category: classify the expense, such as Food, Transport, Shopping,
            Bills, Entertainment, Healthcare, etc.
            - subcategory: more specific classification if possible, otherwise null.
            - note: useful additional information from the receipt, otherwise null.
            - amount: final transaction amount as a number, without ₹ or commas.
            - income_expense: this receipt should normally be "Expense".
            - currency: use "INR".
            - Do not include markdown or ```json.
            """},
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_data
                }
            }
        ]
    )
    return response.text