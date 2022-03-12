import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, NavigationStart, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";
import {filter} from "rxjs/operators";

type Song = {
  "name": string,
  "artist": string,
  "album": string
}

type Playlists = {
  "name": string
}[]

type AutoComplete = [
  {
    "song": string
  }[],
  {
    "artist": string
  }[],
  {
    "album": string
  }[],
]

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  username: string;
  password: string;

  playlists: Playlists;
  listen_again: Song[] | boolean;
  artists: Song[] | boolean;

  autocomplete: AutoComplete;
  searchText: string;

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

  listenAgain() {
    this.http.get("/api/songs/recommend/previous", {
      params: {
        "username": this.username,
        "password": this.password,
      }
    }).forEach(e => {
      if (e) {
        this.listen_again = e! as Song[];
      } else {
        this.listen_again = false;
      }
    }).then()
  }

  fromArtists() {
    this.http.get("/api/songs/recommend/artists", {
      params: {
        "username": this.username,
        "password": this.password,
      }
    }).forEach(e => {
      if (e) {
        this.artists = e! as Song[];
      } else {
        this.artists = false;
      }
    }).then()
  }

  validate(obj: boolean | Song[]) {
    return typeof obj != "boolean";
  }

  autoComplete() {
    if (this.searchText != "") {
      this.http.get("/api/autocomplete", {
        params: {
          "query": this.searchText
        }
      }).forEach(e => {
        if (e) {
          this.autocomplete = e! as AutoComplete;
        }
      }).then()
    } else {
      this.autocomplete = null as AutoComplete;
    }
  }

  ngOnInit() {
    this.router.events.subscribe((e: NavigationStart) => {
      const navigation = this.router.getCurrentNavigation();
      this.username = navigation.extras.state ? navigation.extras.state['username'] : undefined
      this.password = navigation.extras.state ? navigation.extras.state['password'] : undefined
      if (this.username == undefined || this.password == undefined) {
        this.router.navigate(['/login']).then();
      }
      this.getPlaylists()
      this.listenAgain()
      this.fromArtists()
    });
  }

}
