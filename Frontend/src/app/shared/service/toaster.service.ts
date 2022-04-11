import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NotifyService } from './notify.service';

@Injectable({
  providedIn: 'root'
})
/**
 * A utility to show toast messages from anywhere in the application
 */
export class ToasterService {

  public notify: NotifyService;

  constructor(private _notificationService: NotifyService, private snackBar: MatSnackBar) {
    this.notify =  new NotifyService();
    this.notify.SubscribeForContent().subscribe(message => {
      if (message !== undefined) {
        this.snackBar.open(message, 'Ok', {
          verticalPosition: 'top', horizontalPosition: 'end',
          duration: 2000,
        });
      }
  });
  }
}
