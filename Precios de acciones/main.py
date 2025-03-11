import requests as r
from bs4 import BeautifulSoup as bs

#https://www.google.com/finance/quote/ARD-USD
def get_fx_to_usd(currency):
    fx_url = f"https://www.google.com/finance/quote/{currency}-USD"
    resp = r.get(fx_url)
    soup = bs(resp.content, "html.parser")
    fx_rate = soup.find("div", {"data-last-price": True})
    fx = float(fx_rate["data-last-price"])
    
    return fx

#https://www.google.com/finance/quote/AAPL:NASDAQ
def get_price_information(ticker, exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    resp = r.get(url)
    soup = bs(resp.content, "html.parser")
    price_div = soup.find("div", attrs={"data-last-price": True})
    price = float(price_div["data-last-price"])
    currency = (price_div["data-currency-code"])

    usd_price = price
    if currency != "USD":
        fx = get_fx_to_usd(currency)
        usd_price = round(price * fx, 2)

    return {
        'ticker': ticker,
        'exchange': exchange,
        'price': price,
        'currency': currency,
        'usd_price': usd_price
    }

if __name__ == "__main__":
    ticker = "VALO"
    exchange = "BCBA"
    info = get_price_information(ticker, exchange)
    print(info)

    ticker = "SHOP"
    exchange = "TSE"
    info = get_price_information(ticker, exchange)
    print(info)

    ticker = "AAPL"
    exchange = "NASDAQ"
    info = get_price_information(ticker, exchange)
    print(info)