import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import { DashboardService } from 'src/app/service/dashboard.service';
import { SubscriptionService } from 'src/app/service/subscription.service';
import { ToasterService } from 'src/app/shared/service/toaster.service';

import { ChartData, ChartOptions } from 'chart.js';

import { IgxDoughnutChartComponent, IgxRingSeriesComponent,IgxPieChartComponent,IgxLegendComponent } from "igniteui-angular-charts";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit {

  public data: any = [];
  public stock: string = "";
  public showChart: boolean = false;
  public loadDescription: boolean = false;

  public sentiment: any;

  public username: string | null = "";
  public subscriptionList: Array<any> = [];

  public pricePrediction: any;
  public test: ChartData<'line'> = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      { label: 'Mobiles', data: [1000, 1200, 1050, 2000, 500], tension: 0.5 },
      { label: 'Laptop', data: [200, 100, 400, 50, 90], tension: 0.5 },
      { label: 'AC', data: [500, 400, 350, 450, 650], tension: 0.5 },
      { label: 'Headset', data: [1200, 1500, 1020, 1600, 900], tension: 0.5 },
    ],
  };
  chartOptions: ChartOptions = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Price Prediction',
      },
    },
  };

  constructor(private readonly router: ActivatedRoute, 
    private navigateRouter: Router,
    private toasterService: ToasterService,
    private subscriptionService: SubscriptionService,
    private dataService: DashboardService) {
      this.stock = this.router.snapshot.params['id'];
      this.username = localStorage.getItem('currentUser');
      if (this.username == null || this.username == "") {
        this.navigateRouter.navigate(['/login']);
      }
      this.loadData()
      this.GetStockSentiments();
      this.GetStockPrediction();
  }

  subscribeStock() {
    var user: string = this.username!;
    if (this.subscriptionList.includes(this.stock)) {
      this.subscriptionList.forEach((element,index)=>{
        if(element==this.stock) this.subscriptionList.splice(index,1);
      });
    } else {
      this.subscriptionList.push(this.stock);
    }
    
    this.subscriptionService.AddStockToUserSubscription(user, this.subscriptionList).subscribe({
      next: (response: any) => {
        this.toasterService.notify.UpdateContent("Successful!")
      }
    });
  }

  loadData() {
    
    this.dataService.GET_STOCK_DETAILS(this.stock).subscribe({
      next: (response: any) => {
        let priceList: any = []
         
        response['prices'].forEach((element:any) => {
          let obj = {
            "time": new Date(element["date"]),
            "open": element["open"],
            "high": element["high"],
            "low": element["low"],
            "close": element["close"],
            "volume": element["volume"]
          }
          priceList.push(obj);
        });
        this.data.push(priceList);
        this.showChart = true;
      }
    })
  }

  ngOnInit(): void {
    this.loadDescription = true;
    this.GetUserSubscriptions()
  }

  GetUserSubscriptions() {
    this.subscriptionService.GetSubscription().subscribe({
      next: (response: any) => {
        var stockList = this.get_user_specific_subscriptions(response);
        this.subscriptionList = stockList;
      }
    })
  }

  GetStockSentiments() {
    this.subscriptionService.GetStockSentiment().subscribe({
      next: (response: any) => {
        response["Items"].forEach((element:any) => {
          if (element["stock_symbol"]["S"] == this.stock) {
            this.sentiment = {
              "variation_plot": element["detailed_plot"]["S"],
              "sentiment": element["stock_sentiment"]["S"]
            };
          }
        });
      }
    })
  }

  GetStockPrediction() {
    this.dataService.GET_STOCK_PREDICTION(this.stock).subscribe({
      next: (response: any) => {
        var pricePrediction: any = {labels: [], datasets:[{label:this.stock, data:[]}]};
        if ('prices' in response) {
          response["prices"].forEach((element:any) => {
              pricePrediction["labels"].push(element["date"]);
              pricePrediction["datasets"][0]["data"].push(element["0.5"]);
          });
          this.pricePrediction = pricePrediction;
        }
      }
    })
  }

  get_user_specific_subscriptions(data: any) : Array<string> {
    var items = data['Items'];
    var stocksList: Array<string> = []
    if (items.length > 0) {
      items.forEach((element:any) => {
        if (element["username"]["S"] == this.username) {
          var subscribedStocks = element["stock_symbol"]["L"]
          if (subscribedStocks && subscribedStocks.length > 0) {
            subscribedStocks.forEach((subscribedStock: any) => {
              stocksList.push(subscribedStock["S"]);
            });
          }
        }
      });
    }
    return stocksList;
  }

}
