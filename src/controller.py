import pandas as pd
import os


def read_csv_from_resources(file_name):
    return pd.read_csv(os.path.join("resources", file_name))


def get_all_information():
    df = read_csv_from_resources("info.csv")
    json = df.to_json(orient="records")
    return json


def get_company_information(company_ticker):
    df = read_csv_from_resources("info.csv")
    json = df.loc[df.symbol == company_ticker].to_json(orient="records")
    return json


def get_company_price_history(company_ticker):
    df = read_csv_from_resources("historical.csv")
    json = df.loc[df.Ticker == company_ticker].to_json(orient="records")
    return json
