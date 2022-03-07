import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

type Playlists = {
  "name": string
}[];

type Song = {
  "name": string,
  "artist": string,
  "album": string,
  "genre": string,
  "listen_count": number
}

@Component({
  selector: 'app-song',
  templateUrl: './song.page.html',
  styleUrls: ['./song.page.scss'],
})
export class SongPage implements OnInit {

  username: string;
  password: string;
  song: Song;
  playlists: Playlists;
  selected_playlist: string;

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) { }

  loadSong(name: string) {
    this.http.get("/api/songs/get", {
      params: {
        "name": name,
        "username": this.username,
        "password": this.password,
      }
    }).forEach(e => {
      this.song = e! as Song;
    })
  }

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

  addToPlaylist() {
    console.log(this.selected_playlist)
    this.http.post('/api/playlists/songs/add', null, {
      params: {
        "name": this.selected_playlist,
        "song": this.song.name,
        "username": this.username,
        "password": this.password,
      }
    }).forEach(_ => {}).then()
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.password = params['password'];
      this.username = params['username'];
      let song = this.route.snapshot.paramMap.get("song")
      if (this.username == undefined || this.password == undefined || song == undefined) {
        this.router.navigate(['/login']).then();
      }
      this.loadSong(song);
      this.getPlaylists();
    })
  }

}
