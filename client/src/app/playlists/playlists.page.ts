import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

type Playlists = {
  "name": string
}[];

type Playlist = {
  "name": string,
  "artist": string,
  "date": string
}

@Component({
  selector: 'app-playlists',
  templateUrl: './playlists.page.html',
  styleUrls: ['./playlists.page.scss'],
})
export class PlaylistsPage implements OnInit {

  public username: string;
  public password: string;

  public playlist_name: string;
  public playlist: Playlist;
  public playlists: Playlists;

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
      this.password = params['password'];
      this.username = params['username'];
      if (this.username == undefined || this.password == undefined) {
        this.router.navigate(['/login']).then();
      }
      this.getPlaylists();
    })
  }

}
