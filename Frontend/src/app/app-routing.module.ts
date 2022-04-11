import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DetailComponent } from './dashboard/home/detail/detail.component';
import { HomeComponent } from './dashboard/home/home.component';
import { LayoutComponent } from './dashboard/layout/layout/layout.component';
import { SubscriptionComponent } from './dashboard/subscription/subscription/subscription.component';
import { LoginComponent } from './login/login/login.component';
import { RegisterComponent } from './login/register/register.component';

const routes: Routes = [{
  path: '',
  component: LoginComponent
}, {
  path: 'login',
  component: LoginComponent
}, {
  path: 'register',
  component: RegisterComponent
}, {
  path: 'dashboard',
  component: LayoutComponent,
  children: [
    {
      path: '',
      component: HomeComponent
    },
    {
      path: 'stock/:id', component: DetailComponent,
      // canActivate: [AuthGuard],
    },
    {
      path: 'subscriptions', component: SubscriptionComponent,
      // canActivate: [AuthGuard],
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
