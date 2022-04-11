import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DashboardService } from 'src/app/service/dashboard.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  public data: any = [];
  public username: string | null = "";
  
  constructor(private router: Router, private dataService: DashboardService) {
    this.username = localStorage.getItem('currentUser');
      if (this.username == null || this.username == "") {
        this.router.navigate(['/login']);
      }
    this.loadData()
  }

  loadData() {
    this.dataService.GET_STOCK_DETAILS("S&P").subscribe({
      next: (response: any) => {
        this.data.push(response);
      }
    })
  }

  ngOnInit(): void {
  }

}
