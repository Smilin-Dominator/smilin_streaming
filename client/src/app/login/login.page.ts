import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  login = true;
  artist = false;
  showHeader = false;

  artist_name: string = "";
  username: string = "";
  password: string = "";

  constructor(private http: HttpClient, private router: Router, private route: ActivatedRoute) {}

  user_login() {
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

  artist_login() {
    if (this.username.length != 0 && this.password.length != 0 && this.artist_name.length != 0) {
      this.http.post("/api/artists/login", null, {
        params: {
          "username": this.username,
          "password": this.password
        }
      }).forEach(e => {
        if (e != false) {
          this.router.navigate(['/artist', this.artist_name], {
            queryParams: {
              "username": this.username,
              "password": this.password,
              "artist": true
            }
          }).then()
        }
      }).then()
    }
  }

  artist_register() {
    if (this.username.length != 0 && this.password.length != 0 && this.artist_name.length != 0) {
      this.http.post("/api/artists/register", null, {
        params: {
          "name": this.artist_name,
          "username": this.username,
          "password": this.password
        }
      }).forEach(e => {
        if (e != false) {
          this.router.navigate(['/artist', this.artist_name], {
            queryParams: {
              "username": this.username,
              "password": this.password,
              "artist": true
            }
          }).then()
        }
      }).then()
    }
  }

  user_register() {
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
              "password": this.password,
              "artist": true
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
      this.artist = params['artist'] as boolean;
      if (this.username != undefined || this.password != undefined) {
        this.showHeader = true;
      }
    })
  }

}
