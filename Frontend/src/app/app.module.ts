import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http'

import { MatButtonModule } from '@angular/material/button'
import { MatMenuModule } from '@angular/material/menu'
import { MatInputModule } from '@angular/material/input'
import { MatCheckboxModule } from '@angular/material/checkbox'
import { MatSnackBarModule} from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon'
import { MatToolbarModule } from '@angular/material/toolbar'
import { MatTabsModule} from '@angular/material/tabs';
import { MatListModule} from '@angular/material/list';
import { MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatAutocompleteModule} from '@angular/material/autocomplete';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LoginComponent } from './login/login/login.component';
import { RegisterComponent } from './login/register/register.component';
import { HomeComponent } from './dashboard/home/home.component';
import { HeaderComponent } from './shared/header/header.component';
import { InterceptorService } from './interceptor';
import { LayoutComponent } from './dashboard/layout/layout/layout.component';
import { TopNavComponent } from './dashboard/layout/layout/top-nav/top-nav.component';
// import { ChartsModule } from 'ng2-charts';
import { IgxFinancialChartModule, IgxLegendModule, IgxCategoryChartModule } from "igniteui-angular-charts";
import { IgxLineSeriesModule } from 'igniteui-angular-charts';
import { IgxCategoryXAxisModule } from 'igniteui-angular-charts';
import { IgxNumericYAxisModule } from 'igniteui-angular-charts';

import { IgxDataChartCoreModule } from 'igniteui-angular-charts';
import { IgxDataChartCategoryModule } from 'igniteui-angular-charts';
import { DetailComponent } from './dashboard/home/detail/detail.component';
import { SubscriptionComponent } from './dashboard/subscription/subscription/subscription.component';
import { NgChartsModule } from 'ng2-charts';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    HeaderComponent,
    LayoutComponent,
    TopNavComponent,
    DetailComponent,
    SubscriptionComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    RouterModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatInputModule,
    MatMenuModule,
    MatCheckboxModule,
    MatSnackBarModule,
    MatIconModule,
    MatToolbarModule,
    MatTabsModule,
    MatSlideToggleModule,
    MatListModule,
    MatAutocompleteModule,
    IgxFinancialChartModule,
	  IgxLegendModule,
    IgxCategoryChartModule,
    IgxLineSeriesModule,
    IgxCategoryXAxisModule,
    IgxNumericYAxisModule,
    IgxDataChartCoreModule,
    IgxDataChartCategoryModule,
    NgChartsModule
  ],
  providers: [
    // AuthGuard,
    {
    provide: HTTP_INTERCEPTORS,
    useClass: InterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
