import { HttpClient, HttpBackend, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiConstants } from '../app.constants';

@Injectable({
  providedIn: 'root'
})
/**
 * A user-service created to interact with the backend server for user related functionalities.
 */
export class UserService {

  constructor(public http: HttpClient, public httpBackend: HttpBackend, private constants: ApiConstants) { }

  public SIGN_IN(user:any) {
    const url = this.constants.BaseUrl + "login/"
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
    return this.http.post(url, user, {headers:headers});
  }

  public REGISTER(user:any) {
    const url = this.constants.BaseUrl + "signup"
    return this.http.post(url, user);
  }

  public logout() {
    const url = this.constants.BaseUrl + "user/logout"
    return this.http.get(url);
  }
}
