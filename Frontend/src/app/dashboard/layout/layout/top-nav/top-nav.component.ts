import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { map, Observable, startWith } from 'rxjs';
import { Stock } from 'src/app/models/stock';
import { DashboardService } from 'src/app/service/dashboard.service';
import { UserService } from 'src/app/service/user.service';
import {NotifyService} from 'src/app/shared/service/notify.service'
import { ToasterService } from 'src/app/shared/service/toaster.service';

@Component({
  selector: 'app-top-nav',
  templateUrl: './top-nav.component.html',
  styleUrls: ['./top-nav.component.scss']
})
export class TopNavComponent implements OnInit {
  @Output() sideNavToggled = new EventEmitter<void>();
  @Output() searchTrigger = new EventEmitter<String>();

  searchValue: String = "";
  loggedInUser: String = "";
  stocksList: Stock[] = [];
  stateCtrl = new FormControl();
  filteredStocks: Observable<Stock[]>;
  
  constructor(private readonly router: Router, private notifyService: NotifyService, private userService: UserService,
    private dashboardService: DashboardService,
    private toasterService: ToasterService,) {
      this.getStocksList();
      this.filteredStocks = this.stateCtrl.valueChanges.pipe(
        startWith(''),
        map((stock: string) => (stock ? this._filterStocks(stock) : this.stocksList.slice())),
      );
    }
  
    private _filterStocks(value: string) {
      const filterValue = value.toLowerCase();
      return this.stocksList.filter(stock => stock.name.toLowerCase().includes(filterValue));
    }

  ngOnInit() {
    if (null !== localStorage.getItem('currentUser')) {
      this.loggedInUser = localStorage.getItem('currentUser')!.toUpperCase();
    }
  }

  toggleSidebar() {
    this.sideNavToggled.emit();
  }

  searchStock(stockId: any) {
    console.log(stockId);
    let url = "/dashboard/stock/" + stockId
    this.router.navigate([url])
    .then(() => {
      window.location.reload();
    });
    // this.router.navigate([url]);
  }

  getStocksList() {
    this.dashboardService.GET_STOCKS().subscribe({
      next: (response: any) => {
        this.stocksList = response;
      },
      error: (error) => {
        this.toasterService.notify.UpdateContent("FAILED To Load Stocks!")
      },
    })
  }

  search() {
    this.notifyService.UpdateContent(this.searchValue);
    this.searchTrigger.emit(this.searchValue);
  }

  onLoggedout() {
    localStorage.removeItem('currentUser');
    this.logout();
    this.router.navigate(['/login']);
  }

  logout() {
    this.userService.logout()
    .subscribe(
      response => {},
      error => {
        this.toasterService.notify.UpdateContent("User Logged Out!");
      });
  }
}
