import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DepartmentHomeComponent } from './home/Department-home.component';
import { DepartmentNewComponent } from './new/Department-new.component';
import { DepartmentDetailComponent } from './detail/Department-detail.component';

const routes: Routes = [
  {path: '', component: DepartmentHomeComponent},
  { path: 'new', component: DepartmentNewComponent },
  { path: ':Id', component: DepartmentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Department-detail-permissions'
      }
    }
  },{
    path: ':DepartmentId/Department', loadChildren: () => import('../Department/Department.module').then(m => m.DepartmentModule),
    data: {
        oPermission: {
            permissionId: 'Department-detail-permissions'
        }
    }
},{
    path: ':OnLoanDepartmentId/Employee', loadChildren: () => import('../Employee/Employee.module').then(m => m.EmployeeModule),
    data: {
        oPermission: {
            permissionId: 'Employee-detail-permissions'
        }
    }
},{
    path: ':WorksForDepartmentId/Employee', loadChildren: () => import('../Employee/Employee.module').then(m => m.EmployeeModule),
    data: {
        oPermission: {
            permissionId: 'Employee-detail-permissions'
        }
    }
}
];

export const DEPARTMENT_MODULE_DECLARATIONS = [
    DepartmentHomeComponent,
    DepartmentNewComponent,
    DepartmentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DepartmentRoutingModule { }