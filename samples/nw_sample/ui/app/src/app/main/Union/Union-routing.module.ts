import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UnionHomeComponent } from './home/Union-home.component';
import { UnionNewComponent } from './new/Union-new.component';
import { UnionDetailComponent } from './detail/Union-detail.component';

const routes: Routes = [
  {path: '', component: UnionHomeComponent},
  { path: 'new', component: UnionNewComponent },
  { path: ':Id', component: UnionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Union-detail-permissions'
      }
    }
  },{
    path: ':UnionId/Employee', loadChildren: () => import('../Employee/Employee.module').then(m => m.EmployeeModule),
    data: {
        oPermission: {
            permissionId: 'Employee-detail-permissions'
        }
    }
}
];

export const UNION_MODULE_DECLARATIONS = [
    UnionHomeComponent,
    UnionNewComponent,
    UnionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UnionRoutingModule { }