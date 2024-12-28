import pandas as pd
import requests
import os


def download_files(csv_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        try:
            bank_name = row['Bank Name']
            account_holder = row['Account Holder Name']
            file_id = row['PDF'].split('/')[-2] 
            
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            output_file = os.path.join(output_folder, f"{bank_name}_{account_holder}.pdf")

            print(f"Downloading file for {account_holder}...")
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Successfully downloaded file for {account_holder}")
            else:
                print(f"Failed to download file for {account_holder}. HTTP Status: {response.status_code}")
        except Exception as e:
            print(f"Error downloading file for {account_holder}: {e}")


if __name__ == "__main__":
    CSV_PATH = 'sheet.csv'
    OUTPUT_FOLDER = 'pdfs'
    download_files(CSV_PATH, OUTPUT_FOLDER)
