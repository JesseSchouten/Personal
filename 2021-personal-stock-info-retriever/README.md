# Description

This project was created to retrieve basic info (e.g. P/E, forward P/E, growth estimates) for a large number of stocks. Specifically to analyze basic info for all the holdings in my ETF's.
To be written to a spreadsheet, and analyzed further. Most online stocker screeners required a paid subscription to make decent exports with basic info, or do not allow to retrieve info for a specific large list of stocks.

start date: 2021-07-31

# Requirements:

- Anaconda3

# Setup:

- Open your anaconda prompt (or editor of choice, e.g. PyCharm or Visual Studio Code)
- Set up your python virtual environment in /2021-personal-stock-info-retriever with the command: python -m venv venv
- Activate your virtual environment, on windows 10: venv/Scripts/activate.ps1
- run: pip install requirements.txt
- run: python main.py

Note: all input files will be loaded from the /input directory, and the output files will be written to the /output directory.
