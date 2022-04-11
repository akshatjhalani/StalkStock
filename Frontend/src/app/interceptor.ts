import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpSentEvent, HttpHeaderResponse, HttpHeaders, } from '@angular/common/http';
import {HttpResponse, HttpUserEvent, HttpErrorResponse, HttpProgressEvent } from '@angular/common/http';
import { Observable, EMPTY, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable()
/**
 * An interceptor created to attach cookies / tokens to
 * every outgoing HTTP request
 */
export class InterceptorService implements HttpInterceptor {

    constructor(public router: Router) {}

    addCommonHttpOptions(request: any): HttpRequest<any> {
      const headerSettings: {[name: string]: string | string[]; } = {};

      for (const key of request.headers.keys()) {
        headerSettings[key] = request.headers.getAll(key);
      }
      // let token = localStorage.getItem('currentUser')
      // headerSettings['Authorization'] = 'Bearer ' + token;
      // headerSettings['Content-Type'] = 'application/json';
      // const newHeader = new HttpHeaders(headerSettings);
      const req = request.clone();
      // req.withCredentials = true;
      return req;
    }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpSentEvent |
    HttpHeaderResponse | HttpProgressEvent | HttpResponse<any> | HttpUserEvent<any>> {
        const custom_request = this.addCommonHttpOptions(req);
        return next.handle(custom_request).pipe(

          catchError( err => {
               if (err.status === 401) {
                    localStorage.removeItem('currentUser');
                    // location.reload(true);
                    this.router.navigate(['login']);
                    // window.location.href = this.environment.config.idmLogOutUrl + currentLocation;
                   return EMPTY;
               } else {
                   return throwError(err);
               }
          })
      );
    }
  }
