import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from 'src/app/service/user.service';
import { ToasterService } from 'src/app/shared/service/toaster.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;
  public loginInvalid: boolean = false;
  loading: boolean = false;
  isLogin: boolean = true;

  constructor(private router: Router,
    private toasterService: ToasterService,
    private userService: UserService,
    private formBuilder: FormBuilder
    ) { 
      this.loginForm = this.formBuilder.group({
        email: ['', Validators.required],
        password: ['', Validators.required]
      });
    }

  ngOnInit() {
    
  }

  get lf() { return this.loginForm.controls; }
  loginBtn() {
    let data = {
      'username': this.lf['email'].value,
      'password': this.lf['password'].value
    }
    if (this.loginForm.valid) {
      this.loading = true;
      const api_handler = this.userService.SIGN_IN(data)
        .subscribe({
        next: (response: any) => {
          localStorage.setItem('currentUser', response['username']);
          localStorage.setItem('token', response['token']);
          this.toasterService.notify.UpdateContent("Welcome " + response['username'] + " !")
          this.router.navigate(['/dashboard']);
        },
        error: (error) => {
          this.toasterService.notify.UpdateContent("LOGIN FAILED!")
        },
        complete: () => this.loading = false
      })
      api_handler.add(() => this.loading = false);
    }
  }

}
