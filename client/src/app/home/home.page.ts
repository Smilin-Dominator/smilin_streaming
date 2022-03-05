import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

type Song = {
  "name": string,
  "artist": string,
  "album": string
  "date": string
}

type Playlists = {
  "name": string
}[]

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  username: string;
  password: string;

  playlists: Playlists;

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) {}

  getPlaylists() {
    this.http.get("/api/playlists/list", {
      params: {
        "username": this.username,
        "password": this.password,
      }
    }).forEach(e => {
      this.playlists = e! as Playlists;
    }).then()
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'];
      this.password = params['password'];
      if (this.username == undefined || this.password == undefined) {
        this.router.navigate(['/login']).then();
      }
    })
    this.getPlaylists()
  }

}
