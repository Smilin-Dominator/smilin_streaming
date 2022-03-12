import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, NavigationStart, Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

type Playlists = {
  "name": string
}[];

@Component({
  selector: 'app-playlists',
  templateUrl: './playlists.page.html',
  styleUrls: ['./playlists.page.scss'],
})
export class PlaylistsPage implements OnInit {

  public username: string;
  public password: string;
  public playlists: Playlists;

  public new_playlist_name: string;

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

  createPlaylist() {
    if (this.new_playlist_name.length != undefined) {
      this.http.post("/api/playlists/create", null, {
        params: {
          "username": this.username,
          "password": this.password,
          "name": this.new_playlist_name
        }
      }).forEach(e => {
        if (e) {
          this.getPlaylists();
        }
      }).then()
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
      this.getPlaylists();
    });
  }

}
