import csv
from bs4 import BeautifulSoup
import requests

class YahooStockScraper:
    def __init__(self) -> None:
        # Initialize the YahooStockScraper with symbols and companies from the NASDAQ CSV file
        with open("data/stock/nasdaq.csv", encoding='utf-8') as f:
            linereader = csv.DictReader(f, delimiter=',', quotechar='"')
            self.symbols = []
            self.companies = []
            for row in linereader:
                self.symbols.append(row['Symbol'])
                self.companies.append(row['Name'])

    def get_symbol(self, name):
        # Get the stock symbol for a given company name
        for i, c in enumerate(self.companies):
            words = c.split()
            if name.lower() in [w.lower() for w in words]:
                return self.symbols[i]
        return name

    def get_stock(self, name):
        # Get stock information from Yahoo Finance based on the provided stock name
        try:
            symbol = self.get_symbol(name)
            page = requests.get(f"https://finance.yahoo.com/quote/{symbol}")
            parsed_page = BeautifulSoup(page.text, 'html.parser')
            quote_summary = parsed_page.find("div", {"id": "quote-summary"})
            tables = quote_summary.find_all("table")
            data = []
            for t in tables:
                table_raws = t.find_all("tr")
                for r in table_raws:
                    title = r.find_all("td")[0].get_text() + ":"
                    value = r.find_all("td")[1].get_text()
                    data.append([title, value])
            return (symbol, self.create_table(data))
        except:
            return (None, None)

    def create_table(self, data):
        """
        Create a formatted table from the extracted stock data.

        Parameters:
        - data (list): List of lists containing stock data.

        Returns:
        - str: Formatted table as a string.
        """

        # Determine the maximum width of each column
        col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

        # Initialize variables for building the formatted table
        text = ""
        result = ""

        # Iterate through data rows and format the table
        for i, row in enumerate(data[1:]):
            row_str = "".join("{:<{}}".format(item, width) for item, width in zip(row, col_widths))
            text += row_str + " " * 5 + "|"

            # Add a horizontal line after every second row
            if i + 1 == 2 * (i // 2) + 2:
                result += text + "\n" + "-" * len(text) + "\n"
                text = ""

        return result
