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
  public description: Description;

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) { }

  describeArtist(artist: string) {
    this.http.get("/api/artists/get", {
      params: {
        "name": artist
      }
    }).forEach(e => {
      this.description = e! as Description
      console.log(this.description)
    }).then()
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.password = params['password'];
      this.username = params['username'];
      let artist = this.route.snapshot.paramMap.get("artist")
      if (this.username == undefined || this.password == undefined || artist == undefined) {
        this.router.navigate(['/login']).then();
      }
      this.describeArtist(artist)
    })
  }

}
