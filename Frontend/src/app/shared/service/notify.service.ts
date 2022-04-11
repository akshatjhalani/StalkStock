import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
/**
 * A notifaction service implemented using observable design pattern.
 * Used to notify the subscribers about an event.
 */
export class NotifyService {

  private content = new Subject<any>();

  constructor() { }

  UpdateContent(data: any) {
    this.content.next(data);
  }

  SubscribeForContent(): Observable<any> {
    return this.content.asObservable();
  }

  ClearContent() {
    this.content.next("");
  }
}
