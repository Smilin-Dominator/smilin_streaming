import { Component, OnInit, ViewChild } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {ActivatedRoute, Router} from "@angular/router";
import { Howl } from "howler";
import {IonRange} from '@ionic/angular';

type Song = {
  "name": string,
  "artist": string,
  "album": string
  "date": string
}

type Playlist = Song[];

@Component({
  selector: 'app-playlist',
  templateUrl: './playlist.page.html',
  styleUrls: ['./playlist.page.scss'],
})
export class PlaylistPage implements OnInit {

  username: string;
  password: string;
  playlist_name: string;
  playlist: Playlist = [];

  player: Howl;
  public song: Song;
  public isPlaying = false;
  public progress = 0;
  @ViewChild('range', {static: false}) range: IonRange;


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

  removeSong(song: string) {
    this.http.post("/api/playlists/songs/delete", null, {
      params: {
        "username": this.username,
        "password": this.password,
        "name": this.playlist_name,
        "song": song
      }
    }).forEach(e => {
      if (e) {
        this.describePlaylist();
      }
    }).then()
  }

  playSong(song: Song) {

    const spaces = (a: string) => {
      return a.replaceAll(" ", "%20")
    }

    let url = `/api/songs/listen?username=${spaces(this.username)}&password=${spaces(this.password)}&song=${spaces(song.name)}`

    if (this.player) {
      this.isPlaying = false;
      this.song = undefined;
      this.player.stop()
    }
    this.player = new Howl({
      src: url,
      format: 'mp3',
      xhr: {
        method: 'GET',
      }
    })
    this.player.play()
    this.isPlaying = true;
    this.song = song;
  }

  pause() {
    this.player.pause()
  }

  play() {
    this.player.play()
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