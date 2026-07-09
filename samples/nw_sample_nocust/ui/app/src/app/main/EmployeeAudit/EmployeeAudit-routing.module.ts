import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmployeeAuditHomeComponent } from './home/EmployeeAudit-home.component';
import { EmployeeAuditNewComponent } from './new/EmployeeAudit-new.component';
import { EmployeeAuditDetailComponent } from './detail/EmployeeAudit-detail.component';

const routes: Routes = [
  {path: '', component: EmployeeAuditHomeComponent},
  { path: 'new', component: EmployeeAuditNewComponent },
  { path: ':Id', component: EmployeeAuditDetailComponent,
    data: {
      oPermission: {
        permissionId: 'EmployeeAudit-detail-permissions'
      }
    }
  }
];

export const EMPLOYEEAUDIT_MODULE_DECLARATIONS = [
    EmployeeAuditHomeComponent,
    EmployeeAuditNewComponent,
    EmployeeAuditDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EmployeeAuditRoutingModule { }