import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from 'src/app/service/user.service';
import { ToasterService } from 'src/app/shared/service/toaster.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;
  public loginInvalid: boolean = false;
  loading: boolean = false;
  isLogin: boolean = true;

  constructor(private router: Router,
    private toasterService: ToasterService,
    private userService: UserService,
    private formBuilder: FormBuilder) { 
      this.registerForm = this.formBuilder.group({
        name: ['', Validators.required],
        email: ['', Validators.required],
        password: ['', Validators.required]
      });
    }

  ngOnInit(): void {
  }

  get rf() { return this.registerForm.controls; }
  registerBtn() {
    let data = {
      'username': this.rf['name'].value,
      'email': this.rf['email'].value,
      'password': this.rf['password'].value
    }
    if (this.registerForm.valid) {
      this.loading = true;
      const api_handler = this.userService.REGISTER(data)
        .subscribe({
        next: (response: any) => {
          this.toasterService.notify.UpdateContent("Registered Successfully.")
          this.router.navigate(['/login']);
        },
        error: (error) => {
          this.toasterService.notify.UpdateContent("REGISTRATION FAILED: Password must contain a uppercase, number and special character!")
        },
        complete: () => this.loading = false
      })
      api_handler.add(() => this.loading = false);
    }
  }

}
