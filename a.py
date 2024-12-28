import os
from dotenv import load_dotenv
import pdfplumber
import pandas as pd
import json
import google.generativeai as genai
from typing import List, Dict

load_dotenv()

class BankStatementGeminiProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def query_gemini(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            print("Raw Gemini Response:", response)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return ""

    def clean_response(self, response: str) -> str:
        if response.startswith("```json") and response.endswith("```"):
            response = response[7:-3].strip()  
        return response

    def process_statement(self, pdf_path: str) -> List[Dict]:
        text = self.extract_text_from_pdf(pdf_path)
        prompt = f"""
        Extract and return a JSON array of banking transactions with these fields:
        - date: transaction date
        - description: transaction description
        - debit: amount debited (0 if credit transaction)
        - credit: amount credited (0 if debit transaction)
        - balance: running balance after transaction

        Text: {text[:3500]}

        Only return the JSON array.
        """
        response = self.query_gemini(prompt)
        response = self.clean_response(response)  
        try:
            transactions = json.loads(response)
            return transactions
        except json.JSONDecodeError:
            print(f"Error: Failed to parse response as JSON. Response received:\n{response}")
            return []

    def save_to_csv(self, transactions: List[Dict], output_path: str, folder_name: str):
        if not transactions:
            print("No transactions to save.")
            return
        df = pd.DataFrame(transactions)
        df["folder"] = folder_name 
        df.to_csv(output_path, index=False)
        print(f"Saved {len(transactions)} transactions to {output_path}")


def process_folder_of_statements(pdf_folder: str, output_folder: str, api_key: str):
    processor = BankStatementGeminiProcessor(api_key)

    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(pdf_folder):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file_name)
            output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.csv")
            folder_name = os.path.basename(pdf_folder)
            print(f"Processing {pdf_path}...")
            transactions = processor.process_statement(pdf_path)
            processor.save_to_csv(transactions, output_path, folder_name)


if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("API_KEY is not set in the .env file")

    pdf_folder = "C:\\Users\\Gaurav\\Desktop\\task\\pdfs"
    output_folder = "C:\\Users\\Gaurav\\Desktop\\task\\output"
    process_folder_of_statements(pdf_folder, output_folder, API_KEY)
