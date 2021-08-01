
# standard library imports
import sys
import os

# third party imports
import csv
import pandas as pd

# own imports
from retriever_objects import StockInfoRetriever


def main(tickers_list, output_file):
    df = pd.DataFrame()
    for ticker in tickers_list:
        print("start {}".format(ticker))
        stock = StockInfoRetriever()
        stock.run(ticker, False)
        stock_info = stock.return_stock_info()
        df = df.append(stock_info, ignore_index=True)
    df.to_csv("output/" + output_file)


if __name__ == "__main__":
    """
    This program will retrieve basic info from yahoo.finance for a given list of stock tickers.
    """
    cwd = os.getcwd().replace("\\", '/')

    input_type = input(
        "What type of input do you want to use? (manual or csv):\n")

    if input_type not in ['manual', 'csv']:
        sys.exit("ERROR - input type not supported")

    if input_type == "manual":
        tickers = input(
            "Enter your list of stock tickers (using a comma as seperator):\n")

        tickers_list = tickers.replace(" ", "").split(",")
    elif input_type == "csv":
        print("\nThe default directory is input.")
        file_name = input(
            "From which file do you want to retrieve the stock tickers?\n")

        tickers_list = []
        try:
            with open(cwd + "/input/{}".format(file_name), "r", newline='') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')

                for row in reader:
                    tickers_list += row
        except FileNotFoundError as e:
            sys.exit("ERROR - invalid file name!")

    output_file = input(
        "What would you like to call your output file? (end with .csv)\n")

    if '.csv' not in output_file:
        sys.exit("ERROR - invalid output file name, Should end with .csv!")

    print(tickers_list)

    main(tickers_list, output_file)
