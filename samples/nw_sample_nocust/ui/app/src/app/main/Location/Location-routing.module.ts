import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LocationHomeComponent } from './home/Location-home.component';
import { LocationNewComponent } from './new/Location-new.component';
import { LocationDetailComponent } from './detail/Location-detail.component';

const routes: Routes = [
  {path: '', component: LocationHomeComponent},
  { path: 'new', component: LocationNewComponent },
  { path: ':country/:city', component: LocationDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Location-detail-permissions'
      }
    }
  },{
    path: ':City/Order', loadChildren: () => import('../Order/Order.module').then(m => m.OrderModule),
    data: {
        oPermission: {
            permissionId: 'Order-detail-permissions'
        }
    }
}
];

export const LOCATION_MODULE_DECLARATIONS = [
    LocationHomeComponent,
    LocationNewComponent,
    LocationDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LocationRoutingModule { }