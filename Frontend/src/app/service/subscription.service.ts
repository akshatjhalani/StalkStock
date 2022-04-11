import { HttpClient, HttpBackend, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { ApiConstants } from '../app.constants';

@Injectable({
  providedIn: 'root'
})
/**
 * A subscription-service created to manage user suscriptions.
 */
export class SubscriptionService {

  constructor(public http: HttpClient, public httpBackend: HttpBackend, private constants: ApiConstants) { }

  public GetStockDetails(stock: any) {
    //   var data: any = [
    //   {"stock":"AAPL","sector":"Technology","description":"International Business Machines Corporation provides integrated solutions and services worldwide.","recommendation":"hold","prices":{"high":129.97,"low":128.09,"volume":1525946,"open":129.66,"cur_price":128.09,"fiftytwoweekhigh":146.11855,"fiftytwoweeklow":114.56},"news":[{"title":"The Zacks Analyst Blog Highlights Chevron, Devon Energy, International Business Machines, Southern Copper and W. P. Carey","url":"https://finance.yahoo.com/news/zacks-analyst-blog-highlights-chevron-104010813.html"},{"title":"Blackberry Lower on Struggles in Cybersecurity, Auto Software Businesses","url":"https://finance.yahoo.com/news/blackberry-lower-struggles-cybersecurity-auto-091154634.html"},{"title":"How IBM Makes Money: Software, Consulting, Infrastructure","url":"https://finance.yahoo.com/m/5727a73f-535a-3536-8ee3-054ac716332d/how-ibm-makes-money%3A.html"},{"title":"Discover Financial (DFS) Teams Up With IBM to Ease Digital Shift","url":"https://finance.yahoo.com/news/discover-financial-dfs-teams-ibm-191307428.html"},{"title":"Buy These 5 High-Yielding Stocks With More Upside Left","url":"https://finance.yahoo.com/news/buy-5-high-yielding-stocks-115411460.html"},{"title":"10 Web 3.0 Stocks to Buy and Hold for Long Term","url":"https://finance.yahoo.com/news/10-3-0-stocks-buy-204046335.html"},{"title":"Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/tech-workers-urge-companies-join-184810184.html"},{"title":"FOCUS-Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/focus-tech-workers-urge-companies-184247863.html"}],"financials":{"c":["Key","2021-12-31","2021-09-30"],"r":[["Net Income",2333000000.0,1130000000.0],["Gross Profit",5938000000.0,8278000000.0],["Total Revenue",3258000000.0,17618000000.0],["Ebit",460000000.0,1786000000.0],["Interest Expense",-303000000.0,-291000000.0]]}},
    //   {"stock":"Google","sector":"Technology","description":"International Business Machines Corporation provides integrated solutions and services worldwide.","recommendation":"hold","prices":{"high":129.97,"low":128.09,"volume":1525946,"open":129.66,"cur_price":128.09,"fiftytwoweekhigh":146.11855,"fiftytwoweeklow":114.56},"news":[{"title":"The Zacks Analyst Blog Highlights Chevron, Devon Energy, International Business Machines, Southern Copper and W. P. Carey","url":"https://finance.yahoo.com/news/zacks-analyst-blog-highlights-chevron-104010813.html"},{"title":"Blackberry Lower on Struggles in Cybersecurity, Auto Software Businesses","url":"https://finance.yahoo.com/news/blackberry-lower-struggles-cybersecurity-auto-091154634.html"},{"title":"How IBM Makes Money: Software, Consulting, Infrastructure","url":"https://finance.yahoo.com/m/5727a73f-535a-3536-8ee3-054ac716332d/how-ibm-makes-money%3A.html"},{"title":"Discover Financial (DFS) Teams Up With IBM to Ease Digital Shift","url":"https://finance.yahoo.com/news/discover-financial-dfs-teams-ibm-191307428.html"},{"title":"Buy These 5 High-Yielding Stocks With More Upside Left","url":"https://finance.yahoo.com/news/buy-5-high-yielding-stocks-115411460.html"},{"title":"10 Web 3.0 Stocks to Buy and Hold for Long Term","url":"https://finance.yahoo.com/news/10-3-0-stocks-buy-204046335.html"},{"title":"Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/tech-workers-urge-companies-join-184810184.html"},{"title":"FOCUS-Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/focus-tech-workers-urge-companies-184247863.html"}],"financials":{"c":["Key","2021-12-31","2021-09-30"],"r":[["Net Income",2333000000.0,1130000000.0],["Gross Profit",5938000000.0,8278000000.0],["Total Revenue",3258000000.0,17618000000.0],["Ebit",460000000.0,1786000000.0],["Interest Expense",-303000000.0,-291000000.0]]}},
    //   {"stock":"IBM","sector":"Technology","description":"International Business Machines Corporation provides integrated solutions and services worldwide.","recommendation":"hold","prices":{"high":129.97,"low":128.09,"volume":1525946,"open":129.66,"cur_price":128.09,"fiftytwoweekhigh":146.11855,"fiftytwoweeklow":114.56},"news":[{"title":"The Zacks Analyst Blog Highlights Chevron, Devon Energy, International Business Machines, Southern Copper and W. P. Carey","url":"https://finance.yahoo.com/news/zacks-analyst-blog-highlights-chevron-104010813.html"},{"title":"Blackberry Lower on Struggles in Cybersecurity, Auto Software Businesses","url":"https://finance.yahoo.com/news/blackberry-lower-struggles-cybersecurity-auto-091154634.html"},{"title":"How IBM Makes Money: Software, Consulting, Infrastructure","url":"https://finance.yahoo.com/m/5727a73f-535a-3536-8ee3-054ac716332d/how-ibm-makes-money%3A.html"},{"title":"Discover Financial (DFS) Teams Up With IBM to Ease Digital Shift","url":"https://finance.yahoo.com/news/discover-financial-dfs-teams-ibm-191307428.html"},{"title":"Buy These 5 High-Yielding Stocks With More Upside Left","url":"https://finance.yahoo.com/news/buy-5-high-yielding-stocks-115411460.html"},{"title":"10 Web 3.0 Stocks to Buy and Hold for Long Term","url":"https://finance.yahoo.com/news/10-3-0-stocks-buy-204046335.html"},{"title":"Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/tech-workers-urge-companies-join-184810184.html"},{"title":"FOCUS-Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/focus-tech-workers-urge-companies-184247863.html"}],"financials":{"c":["Key","2021-12-31","2021-09-30"],"r":[["Net Income",2333000000.0,1130000000.0],["Gross Profit",5938000000.0,8278000000.0],["Total Revenue",3258000000.0,17618000000.0],["Ebit",460000000.0,1786000000.0],["Interest Expense",-303000000.0,-291000000.0]]}},
    //   {"stock":"AMicroAPL","sector":"Technology","description":"International Business Machines Corporation provides integrated solutions and services worldwide.","recommendation":"hold","prices":{"high":129.97,"low":128.09,"volume":1525946,"open":129.66,"cur_price":128.09,"fiftytwoweekhigh":146.11855,"fiftytwoweeklow":114.56},"news":[{"title":"The Zacks Analyst Blog Highlights Chevron, Devon Energy, International Business Machines, Southern Copper and W. P. Carey","url":"https://finance.yahoo.com/news/zacks-analyst-blog-highlights-chevron-104010813.html"},{"title":"Blackberry Lower on Struggles in Cybersecurity, Auto Software Businesses","url":"https://finance.yahoo.com/news/blackberry-lower-struggles-cybersecurity-auto-091154634.html"},{"title":"How IBM Makes Money: Software, Consulting, Infrastructure","url":"https://finance.yahoo.com/m/5727a73f-535a-3536-8ee3-054ac716332d/how-ibm-makes-money%3A.html"},{"title":"Discover Financial (DFS) Teams Up With IBM to Ease Digital Shift","url":"https://finance.yahoo.com/news/discover-financial-dfs-teams-ibm-191307428.html"},{"title":"Buy These 5 High-Yielding Stocks With More Upside Left","url":"https://finance.yahoo.com/news/buy-5-high-yielding-stocks-115411460.html"},{"title":"10 Web 3.0 Stocks to Buy and Hold for Long Term","url":"https://finance.yahoo.com/news/10-3-0-stocks-buy-204046335.html"},{"title":"Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/tech-workers-urge-companies-join-184810184.html"},{"title":"FOCUS-Tech workers urge companies to join Ukraine's digital blockade of Russia","url":"https://finance.yahoo.com/news/focus-tech-workers-urge-companies-184247863.html"}],"financials":{"c":["Key","2021-12-31","2021-09-30"],"r":[["Net Income",2333000000.0,1130000000.0],["Gross Profit",5938000000.0,8278000000.0],["Total Revenue",3258000000.0,17618000000.0],["Ebit",460000000.0,1786000000.0],["Interest Expense",-303000000.0,-291000000.0]]}}]
    //   return of(data);
      stock = stock.join(" "); 
      var data = {"stock": stock};
      const url = this.constants.BaseUrl + "stock";
      return this.http.post(url, data);
  }

  public GetStockSentiment() {
    const url = this.constants.SubscriptionUrl + "stock-sentiment-and-news";
    return this.http.get(url);
  }
  
  public GetSubscription() {
    // return of(['AAPL']);
    const url = this.constants.SubscriptionUrl + "get-user-stock-info"
    return this.http.get(url);
  }

  public AddStockToUserSubscription(user:any, stocks: Array<string>) {
    const url = this.constants.SubscriptionUrl + "get-user-stock-info";
    var stocksObj: any = []
    stocks.forEach(stock=>{
        stocksObj.push(
            {"S": stock}
        )
    })
    var data = {
        "TableName": "user_info_table",
        "Item": {
            "username": {
                "S": user
            },
            "email": {
                "S": "user@email.com"
            },
            "stock_symbol": {
                "L": stocksObj
            }
        }
    }
    return this.http.post(url, data);
  }
}
