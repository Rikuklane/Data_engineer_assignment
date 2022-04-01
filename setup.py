import os
import sys
import subprocess
from src.data_manipulation import setup_financial_data

# installing requirements
current_dir = os.path.dirname(os.path.realpath(__file__))
requirementsPath = os.path.join(current_dir, 'requirements.txt')
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirementsPath])

# extracting and storing data
print("\nFetching financial data from Yahoo Finance API.")
print("Please hold on, this might take a minute or two.")
setup_financial_data()
print("Data has been extracted and transformed.")
