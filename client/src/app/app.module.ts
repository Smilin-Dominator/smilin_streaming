import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import {LoginPage} from "./login/login.page";
import {HomePage} from "./home/home.page";
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {PlaylistsPage} from "./playlists/playlists.page";

@NgModule({
  declarations: [
    AppComponent,
    LoginPage,
    HomePage,
    PlaylistsPage
  ],
  entryComponents: [],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule, HttpClientModule, FormsModule],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy }],
  bootstrap: [AppComponent],
})
export class AppModule {}
