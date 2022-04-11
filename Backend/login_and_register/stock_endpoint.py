import json
from config import Config
from error_handler.sas_handle_exception import sas_handle_exception
from event_utility import EventUtility

config = Config()
@sas_handle_exception
def lambda_handler_get_stock_details(event, context):
    """
    Endpoint for Stock Information
    params: stock
    """
    import json
    event = EventUtility(event)
    body = event.get_body()
    stocks = body['stock']
    f = open('stock.json')
    data = json.load(f)
    output = []
    for stock_label in stocks.split(" "):
        stock_label = stock_label.upper()
        if stock_label in data:
            output.append(data[stock_label])
    return output



@sas_handle_exception
def lambda_handler_get_stock_details_from_yahoo(event, context):
    """
    Endpoint for Refreshing Stock info in DB
    """
    import yfinance as yf
    event = EventUtility(event)
    body = event.get_body()
    stocks = body['stock']

    tickers = yf.Tickers(stocks)
    response = {}
    for stock_label in stocks.split(" "):
        try:
            stock_label = stock_label.upper()
            stock = tickers.tickers[stock_label]
            info = stock.info
            sector = info.get('sector')
            url = info.get('logo_url', "")
            recommendation = info.get('recommendationKey')
            description = info.get('longBusinessSummary')
            desc_arr = description.split(".")
            if len(desc_arr) > 1:
                if len(desc_arr[0]) > 50:
                    description = desc_arr[0]
                else:
                    description = ".".join(desc_arr[0:2])
            prices = {
                    "high": info.get('dayHigh'),
                    "low": info.get('dayLow'),
                    "volume": info.get('volume'),
                    "open": info.get('open'),
                    "cur_price": info.get('currentPrice'),
                    "fiftytwoweekhigh": info.get('fiftyTwoWeekHigh'),
                    "fiftytwoweeklow": info.get('fiftyTwoWeekLow'),
                }
            financials = {
                "c": ["Key"] + list(map(str,[x.date() for x in list(stock.quarterly_financials.columns)[0:2]])),
                "r": []
            }
            keys = ['Net Income', 'Gross Profit', 'Total Revenue', 'Ebit', 'Interest Expense']
            for k in keys:
                row = [k] + list(stock.quarterly_financials.loc[k])[0:2]
                financials["r"].append(row)

            news = []
            try:
                for elem in stock.news:
                    obj = {
                        "title": elem['title'],
                        "url": elem['link']
                    }
                    news.append(obj)
            except Exception as e:
                print(f"News:{stock_label}")
            response[stock_label] = {
                "stock": stock_label,
                "logo": url,
                "sector": sector,
                "description": description,
                "recommendation": recommendation,
                "prices": prices,
                "news": news,
                "financials": financials
            }
        except Exception as e:
            print(stock_label)
    if len(response) > 0:
        return response
    print(response)



if __name__ == "__main__":
    # response = db.query(Order).all()
    # print(Order.generate_response(response))
    stock = " ".join(["MSFT", "GS", "V", "AXP", "AMGN", "CSCO", "KO", "DIS", "CVX", "DOW", "HON", "WMT", "WBA", "AAPL", "INTC", "HD", "CAT", "NKE", "BA", "MRK", "MMM", "MCD", "PG", "VZ", "IBM", "TRV", "JPM", "UNH", "JNJ", "CRM"])

    event = {'body-json': {'full_name': 'Aditya Jhalani', 'user_name': "aditia",
                           'stock': "aapl ibm",
                           'email': "ad@gmail.com", 'password': "Akshat@1234"},
             'context': {'username': '', 'email': ''}}
    # event['context']['username'] = ''
    # event['context']['email'] =''
    # response = lambda_handler_get_stock_details(event, None)
    # print(response)
    import json

    f = open('stock.json')
    data = json.load(f)
    out = []
    import yfinance as yf
    for k, v in data.items():
        tickers = yf.Ticker(k)
        elem = {"id": v['stock'], "name": tickers.info.get("shortName"), "img": v["logo"]}
        out.append(elem)
    print(out)

    f = open('stock.json')
    data = json.load(f)
    out = {}
    for d in data:
        if len(d['news']) == 0:
            r = lambda_handler_get_stock_details_from_yahoo({'body-json': {"stock":d['stock']}}, None)
            d['news'] = r[d['stock']]["news"]
        out[d['stock']] = d
    print(out)

    # with open('stock.json', 'w') as fp:
    #     json.dump(response, fp)
