import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

type DescriptionForUser = [
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

type DescriptionForArtist = [
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
  public description: DescriptionForUser | DescriptionForArtist;

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
    if (this.isArtist) {
      this.http.get("/api/artists/get/artist", {
        params: {
          "username": this.username,
          "password": this.password,
        }
      }).forEach(e => {
        this.description = e! as DescriptionForArtist
        console.log(this.description)
      }).then()
    } else {
      this.http.get("/api/artists/get/user", {
        params: {
          "username": this.username,
          "password": this.password,
          "name": this.artist
        }
      }).forEach(e => {
        this.description = e! as DescriptionForUser
        console.log(this.description)
      }).then()
    }
  }

  loadFile(event) {
    this.uploadFile = event.target.files[0];
  }

  uploadSong() {

    const not_empty = (a: string) => {return a != "" && a != undefined};

    if (not_empty(this.uploadFile.name) && not_empty(this.uploadAlbum) && not_empty(this.uploadGenre) && not_empty(this.uploadSongname)) {
      let form: FormData = new FormData();
      form.append("song", this.uploadFile);
      this.http.post("/api/songs/upload", form, {
        params: {
          "username": this.username,
          "password": this.password,
          "song_name": this.uploadSongname,
          "album": this.uploadAlbum,
          "genre": this.uploadGenre,
          "filename": this.uploadFile.name
        }
      }).forEach(_ => {}).then(() => this.describeArtist())
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
