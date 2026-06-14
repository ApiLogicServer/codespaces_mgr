import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ShipperHomeComponent } from './home/Shipper-home.component';
import { ShipperNewComponent } from './new/Shipper-new.component';
import { ShipperDetailComponent } from './detail/Shipper-detail.component';

const routes: Routes = [
  {path: '', component: ShipperHomeComponent},
  { path: 'new', component: ShipperNewComponent },
  { path: ':Id', component: ShipperDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Shipper-detail-permissions'
      }
    }
  }
];

export const SHIPPER_MODULE_DECLARATIONS = [
    ShipperHomeComponent,
    ShipperNewComponent,
    ShipperDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ShipperRoutingModule { }