import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrderDetailHomeComponent } from './home/OrderDetail-home.component';
import { OrderDetailNewComponent } from './new/OrderDetail-new.component';
import { OrderDetailDetailComponent } from './detail/OrderDetail-detail.component';

const routes: Routes = [
  {path: '', component: OrderDetailHomeComponent},
  { path: 'new', component: OrderDetailNewComponent },
  { path: ':Id', component: OrderDetailDetailComponent,
    data: {
      oPermission: {
        permissionId: 'OrderDetail-detail-permissions'
      }
    }
  }
];

export const ORDERDETAIL_MODULE_DECLARATIONS = [
    OrderDetailHomeComponent,
    OrderDetailNewComponent,
    OrderDetailDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrderDetailRoutingModule { }