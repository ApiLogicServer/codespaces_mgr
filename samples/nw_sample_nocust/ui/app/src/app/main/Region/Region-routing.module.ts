import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegionHomeComponent } from './home/Region-home.component';
import { RegionNewComponent } from './new/Region-new.component';
import { RegionDetailComponent } from './detail/Region-detail.component';

const routes: Routes = [
  {path: '', component: RegionHomeComponent},
  { path: 'new', component: RegionNewComponent },
  { path: ':Id', component: RegionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Region-detail-permissions'
      }
    }
  }
];

export const REGION_MODULE_DECLARATIONS = [
    RegionHomeComponent,
    RegionNewComponent,
    RegionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RegionRoutingModule { }