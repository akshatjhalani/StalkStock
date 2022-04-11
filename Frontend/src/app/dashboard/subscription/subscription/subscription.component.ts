import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DashboardService } from 'src/app/service/dashboard.service';
import { SubscriptionService } from 'src/app/service/subscription.service';

@Component({
  selector: 'app-subscription',
  templateUrl: './subscription.component.html',
  styleUrls: ['./subscription.component.scss']
})
export class SubscriptionComponent implements OnInit {

  @Input() selectedstock: string="";
  
  public isSubscriptionPage: Boolean = true;
  public username: string | null = "";
  public subscriptionList: Array<any> = [];

  constructor(
    private router: Router,
    private subscriptionService: SubscriptionService,
    private dashboardService: DashboardService
  ) {
      this.username = localStorage.getItem('currentUser');
      if (this.username == null || this.username == "") {
        this.router.navigate(['/login']);
      }
   }

  ngOnInit(): void {
    if (this.selectedstock && this.selectedstock.length > 0) {
      this.isSubscriptionPage = false;
      this.GetStockInfo();
    } else {
      this.GetUserSubscriptions();
    }
  }

  ngAfterViewInit() {
    const activeTabs = document.getElementsByClassName('default-active');
    for (let i = 0; i < activeTabs.length; i++) {
      (<HTMLElement>activeTabs[i]).click();
    }
  }

  GetStockInfo() {
    var stockList = [this.selectedstock];
    this.subscriptionService.GetStockDetails(stockList).subscribe({
      next: (response: any) => {
        this.subscriptionList = response;
      }
    })
  }

  GetUserSubscriptions() {
    this.subscriptionService.GetSubscription().subscribe({
      next: (response: any) => {
        var stockList = this.get_user_specific_subscriptions(response);
        // stockList = ["IBM", "AAPL"]
        this.subscriptionService.GetStockDetails(stockList).subscribe({
          next: (response: any) => {
            this.subscriptionList = response;
          }
        });
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
