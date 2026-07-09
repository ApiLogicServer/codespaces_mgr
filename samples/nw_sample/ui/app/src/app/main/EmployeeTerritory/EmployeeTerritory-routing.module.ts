import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmployeeTerritoryHomeComponent } from './home/EmployeeTerritory-home.component';
import { EmployeeTerritoryNewComponent } from './new/EmployeeTerritory-new.component';
import { EmployeeTerritoryDetailComponent } from './detail/EmployeeTerritory-detail.component';

const routes: Routes = [
  {path: '', component: EmployeeTerritoryHomeComponent},
  { path: 'new', component: EmployeeTerritoryNewComponent },
  { path: ':Id', component: EmployeeTerritoryDetailComponent,
    data: {
      oPermission: {
        permissionId: 'EmployeeTerritory-detail-permissions'
      }
    }
  }
];

export const EMPLOYEETERRITORY_MODULE_DECLARATIONS = [
    EmployeeTerritoryHomeComponent,
    EmployeeTerritoryNewComponent,
    EmployeeTerritoryDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EmployeeTerritoryRoutingModule { }