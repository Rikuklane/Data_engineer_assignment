import yfinance as yf
import logging
import pandas as pd
import os
import asyncio


def setup_financial_data():
    """
    Pre-defined setup func for the project that extracts, transforms and stores data for defined companies
    """
    list_to_extract = ["MSFT", "TSLA", "AAPL", "NVDA", "AMD", "AMZN", "EA", "FB", "GOOG", "WMT", "INTC", "MCD", "NKE"]

    logging.debug("Fetching & Storing financial data from Yahoo Finance API")
    info_df, history_df = asyncio.run(extract_and_transform_all_given_companies(list_to_extract))

    store_financial_data(info_df, history_df)


async def extract_and_transform_all_given_companies(ticker_list: list):
    """
    Extracts (async) and transforms the data for the given list of tickers
    :param ticker_list: list of company tickers to extract data from
    :return: pd.DataFrame, pd.DataFrame
    """
    # if no tickers are provided
    if len(ticker_list) == 0:
        logging.warning("No tickers provided!")
        return pd.DataFrame(), pd.DataFrame()

    # getting all the data async
    info_list = []
    history_dataframes = []

    loop = asyncio.get_event_loop()

    tasks = [loop.run_in_executor(None, extract_yfinance_company, ticker) for ticker in ticker_list]
    results = await asyncio.gather(*tasks)

    # combining the right data together
    for result_tuple in results:
        info_list.append(result_tuple[0])
        history_dataframes.append(result_tuple[1])

    # formatting data to dataframe and removing unnecessary values
    info_df = pd.DataFrame(info_list)
    info_df.set_index("symbol", inplace=True)
    info_df = info_df[[
        "longName", "exchange", "market", "sector", "industry", "fullTimeEmployees", "country", "state",
        "city", "website", "currency", "bookValue", "marketCap", "currentPrice", "targetMedianPrice",
        "dividendYield", "dividendRate", "returnOnAssets", "logo_url"
    ]]
    history_df = pd.concat(history_dataframes)
    history_df.drop(columns=["Dividends", "Stock Splits"], inplace=True)

    return info_df, history_df


def extract_yfinance_company(stock_ticker: str):
    """
    Extracts needed information about the given ticker
    :param stock_ticker: ticker to get data for the specific company
    :return: dict, pd.DataFrame
    """
    # get stock info & historical market data
    company = yf.Ticker(stock_ticker)
    logging.debug(f"Extract YFinance data ({stock_ticker})")
    history = company.history(period="1y")
    history["Ticker"] = stock_ticker
    return company.info, history


def store_financial_data(info: pd.DataFrame, historical: pd.DataFrame):
    """
    Method for storing transformed data into csv files
    :param info:
    :param historical:
    """
    def write_to_csv(df, file_name):
        df.to_csv(os.path.join("resources", file_name))
        logging.debug(f"Wrote new information to 'resources/{file_name}'")

    if info.shape[0] != 0:
        write_to_csv(info, "info.csv")

    if historical.shape[0] != 0:
        write_to_csv(historical, "historical.csv")
