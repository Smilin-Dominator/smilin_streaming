import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  showRegister = false;
  showLogin = true;
  showHeader = false;

  username: string = "";
  password: string = "";

  constructor(private http: HttpClient, private router: Router, private route: ActivatedRoute) {}

  login() {
    if (this.username.length != 0 && this.password.length != 0) {
      this.http.post("/api/users/login", null, {
        params: {
          "username": this.username,
          "password": this.password
        }
      }).forEach(e => {
        if (e != false) {
          this.router.navigate(['/home'], {
            queryParams: {
              "username": this.username,
              "password": this.password
            }
          }).then()
        }
      }).then()
    }
  }

  register() {
    if (this.username.length != 0 && this.password.length != 0) {
      this.http.post("/api/users/register", null, {
        params: {
          "username": this.username,
          "password": this.password
        }
      }).forEach(e => {
        if (e != false) {
          this.router.navigate(['/home'], {
            queryParams: {
              "username": this.username,
              "password": this.password
            }
          }).then()
        }
      }).then()
    }
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'];
      this.password = params['password'];
      if (this.username != undefined || this.password != undefined) {
        this.showHeader = true;
      }
    })
  }

}
