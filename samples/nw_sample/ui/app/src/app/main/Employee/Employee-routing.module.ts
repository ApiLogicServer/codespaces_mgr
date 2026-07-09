import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmployeeHomeComponent } from './home/Employee-home.component';
import { EmployeeNewComponent } from './new/Employee-new.component';
import { EmployeeDetailComponent } from './detail/Employee-detail.component';

const routes: Routes = [
  {path: '', component: EmployeeHomeComponent},
  { path: 'new', component: EmployeeNewComponent },
  { path: ':Id', component: EmployeeDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Employee-detail-permissions'
      }
    }
  },{
    path: ':EmployeeId/EmployeeAudit', loadChildren: () => import('../EmployeeAudit/EmployeeAudit.module').then(m => m.EmployeeAuditModule),
    data: {
        oPermission: {
            permissionId: 'EmployeeAudit-detail-permissions'
        }
    }
},{
    path: ':EmployeeId/EmployeeTerritory', loadChildren: () => import('../EmployeeTerritory/EmployeeTerritory.module').then(m => m.EmployeeTerritoryModule),
    data: {
        oPermission: {
            permissionId: 'EmployeeTerritory-detail-permissions'
        }
    }
},{
    path: ':EmployeeId/Order', loadChildren: () => import('../Order/Order.module').then(m => m.OrderModule),
    data: {
        oPermission: {
            permissionId: 'Order-detail-permissions'
        }
    }
}
];

export const EMPLOYEE_MODULE_DECLARATIONS = [
    EmployeeHomeComponent,
    EmployeeNewComponent,
    EmployeeDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EmployeeRoutingModule { }