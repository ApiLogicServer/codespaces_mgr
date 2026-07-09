import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrderHomeComponent } from './home/Order-home.component';
import { OrderNewComponent } from './new/Order-new.component';
import { OrderDetailComponent } from './detail/Order-detail.component';

const routes: Routes = [
  {path: '', component: OrderHomeComponent},
  { path: 'new', component: OrderNewComponent },
  { path: ':Id', component: OrderDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Order-detail-permissions'
      }
    }
  },{
    path: ':CloneFromOrder/Order', loadChildren: () => import('../Order/Order.module').then(m => m.OrderModule),
    data: {
        oPermission: {
            permissionId: 'Order-detail-permissions'
        }
    }
},{
    path: ':OrderId/OrderDetail', loadChildren: () => import('../OrderDetail/OrderDetail.module').then(m => m.OrderDetailModule),
    data: {
        oPermission: {
            permissionId: 'OrderDetail-detail-permissions'
        }
    }
}
];

export const ORDER_MODULE_DECLARATIONS = [
    OrderHomeComponent,
    OrderNewComponent,
    OrderDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrderRoutingModule { }