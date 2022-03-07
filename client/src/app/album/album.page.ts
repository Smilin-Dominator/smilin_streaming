import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

type Album = [
  {
    name: string
  }[],
  {
    name: string,
    genre: string,
    listen_count: number
  }[]
]

@Component({
  selector: 'app-album',
  templateUrl: './album.page.html',
  styleUrls: ['./album.page.scss'],
})
export class AlbumPage implements OnInit {

  public album: Album;
  public album_name: string;
  public username: string;
  public password: string;

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) { }

  describe() {
    this.http.get("/api/albums/get", {
      params: {
        "name": this.album_name
      }
    }).subscribe(e => this.album = e! as Album)
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.password = params['password'];
      this.username = params['username'];
      this.album_name = this.route.snapshot.paramMap.get("album")
      if (this.username == undefined || this.password == undefined || this.album_name == undefined) {
        this.router.navigate(['/login']).then();
      }
      this.describe()
    })
  }

}
