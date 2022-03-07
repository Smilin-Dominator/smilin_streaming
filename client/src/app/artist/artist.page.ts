import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

type Description = [
  {
    name: string,
    followers: number
  },
  {
    album: string
  }[],
  {
    "name": string,
    "listen_count": number,
    "album": string,
    "genre": string
  }[],
  {
    total_listens: number
  },
  {
    following: boolean
  }
]

@Component({
  selector: 'app-artist',
  templateUrl: './artist.page.html',
  styleUrls: ['./artist.page.scss'],
})
export class ArtistPage implements OnInit {

  username: string;
  password: string;
  artist: string;
  isArtist: boolean;
  public description: Description;

  uploadFile: File;
  uploadSongname: string;
  uploadAlbum: string;
  uploadGenre: string;

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) { }

  toggleFollow() {
    this.http.post("/api/users/toggle_follow", null, {
      params: {
        "username": this.username,
        "password": this.password,
        "name": this.artist
      }
    }).forEach(_ => {}).then(() => this.describeArtist())
  }

  describeArtist() {
    this.http.get("/api/artists/get", {
      params: {
        "username": this.username,
        "password": this.password,
        "name": this.artist
      }
    }).forEach(e => {
      this.description = e! as Description
      console.log(this.description)
    }).then()
  }

  loadFile(event) {
    this.uploadFile = event.target.files[0];
  }

  uploadSong() {

    const not_empty = (a: string) => {return a != "" && a != undefined};

    if (not_empty(this.uploadFile.name) && not_empty(this.uploadAlbum) && not_empty(this.uploadGenre) && not_empty(this.uploadSongname)) {
      this.http.post("/api/songs/upload", {
        "song": this.uploadFile
      }, {
        params: {
          "username": this.username,
          "password": this.password,
          "song_name": this.uploadSongname,
          "album": this.uploadAlbum,
          "genre": this.uploadGenre,
          "filename": this.uploadFile.name
        }
      }).forEach(_ => {}).then()
    }

  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.password = params['password'];
      this.username = params['username'];
      this.isArtist = params['artist'];
      this.artist = this.route.snapshot.paramMap.get("artist")
      if (this.username == undefined || this.password == undefined || this.artist == undefined) {
        this.router.navigate(['/login']).then();
      }
      this.describeArtist()
    })
  }

}
