import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {ActivatedRoute, Router} from "@angular/router";

type Playlist = {
  "name": string,
  "artist": string,
  "date": string
}[]

@Component({
  selector: 'app-playlist',
  templateUrl: './playlist.page.html',
  styleUrls: ['./playlist.page.scss'],
})
export class PlaylistPage implements OnInit {

  username: string;
  password: string;
  playlist_name: string;
  playlist: Playlist;

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) { }

  describePlaylist() {
    this.http.get("/api/playlists/get", {
      params: {
        "username": this.username,
        "password": this.password,
        "name": this.playlist_name
      }
    }).forEach(e => {
      this.playlist = e! as Playlist;
    }).then()
  }

  deletePlaylist() {
    this.http.post("/api/playlists/delete", null, {
      params: {
        "username": this.username,
        "password": this.password,
        "name": this.playlist_name
      }
    }).forEach(e => {
      if (e) {
        this.router.navigate(['/playlists'], {
          queryParams: {
            "username": this.username,
            "password": this.password,
          }
        })
      }
    })
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.password = params['password'];
      this.username = params['username'];
      this.playlist_name = this.route.snapshot.paramMap.get("playlist")
      if (this.username == undefined || this.password == undefined) {
        this.router.navigate(['/login']).then();
      }
      this.describePlaylist();
    })
  }

}
