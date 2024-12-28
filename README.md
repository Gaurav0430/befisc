# Bank Statement Processor Using Gemini API

This project provides a Python-based tool for processing bank statement PDFs. It extracts transaction details, uses the Gemini API to parse the data into structured JSON, and saves the results as CSV files. The tool is designed to handle multiple PDF files efficiently, making it ideal for bulk processing.

---

## Key Features

- **PDF Text Extraction:** Extracts text content from PDFs using the `pdfplumber` library.
- **AI-Powered Data Parsing:** Utilizes the Gemini API to process raw text into structured transaction details.
- **CSV Output:** Saves parsed transactions in CSV format, with folder information for tracking.
- **Batch Processing:** Processes all PDF files in a given folder, making bulk tasks easier.

---

## Prerequisites

- Python 3.8 or higher.
- An active Gemini API key (from Google Generative AI).

---

## There are 2 python files a.py is the main file and gdrive.py is the file to download all pdf files

### Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/bank-statement-processor.git
cd bank-statement-processor
