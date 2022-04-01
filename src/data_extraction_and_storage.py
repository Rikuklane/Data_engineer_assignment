import yfinance as yf
import logging
import pandas as pd
import os


def extract_and_transform_all_given_companies(ticker_list: list):
    # if no tickers are provided
    if len(ticker_list) == 0:
        return pd.DataFrame(), pd.DataFrame()

    # getting all the data
    info_list = []
    history_dataframes = []

    for ticker in ticker_list:
        info, history = extract_yfinance_company(ticker)
        history["Ticker"] = ticker
        info_list.append(info)
        history_dataframes.append(history)

    # formatting data to dataframe
    info_df = pd.DataFrame(info_list)
    info_df.set_index("symbol")
    history_df = pd.concat(history_dataframes)
    history_df.drop(columns=["Dividends", "Stock Splits"], inplace=True)

    return info_df, history_df


def extract_yfinance_company(stock_ticker: str):
    # get stock info & historical market data
    company = yf.Ticker(stock_ticker)
    logging.debug(f"Extract YFinance data ({stock_ticker})")
    return company.info, company.history(period="1y")


def store_financial_data(info: pd.DataFrame, historical: pd.DataFrame):
    if info.shape[0] != 0:
        info.to_csv(os.path.join("data", "info.csv"), index=False)
        logging.debug("Wrote new information to 'data/info.csv'")

    if historical.shape[0] != 0:
        historical.to_csv(os.path.join("data", "historical.csv"))
        logging.debug("Wrote new information to 'data/info.csv'")


def setup_financial_data():
    list_to_extract = ["MSFT", "TSLA", "AAPL", "NVDA", "AMD", "AMZN", "EA", "FB", "GOOG", "WMT", "INTC", "MCD", "NKE"]

    logging.debug("Fetching financial data from Yahoo Finance API")
    info_df, history_df = extract_and_transform_all_given_companies(list_to_extract)

    logging.debug("Storing YFinance data")
    store_financial_data(info_df, history_df)
