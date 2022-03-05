import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PlaylistsPage } from './playlists.page';

const routes: Routes = [
  {
    path: '',
    component: PlaylistsPage,
    children: [
      {
        path: ":playlist",
        loadChildren: () => import('./playlist/playlist.module').then(m => m.PlaylistPageModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PlaylistsPageRoutingModule {}
