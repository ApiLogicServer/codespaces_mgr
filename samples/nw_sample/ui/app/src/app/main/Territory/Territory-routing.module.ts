import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TerritoryHomeComponent } from './home/Territory-home.component';
import { TerritoryNewComponent } from './new/Territory-new.component';
import { TerritoryDetailComponent } from './detail/Territory-detail.component';

const routes: Routes = [
  {path: '', component: TerritoryHomeComponent},
  { path: 'new', component: TerritoryNewComponent },
  { path: ':Id', component: TerritoryDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Territory-detail-permissions'
      }
    }
  },{
    path: ':TerritoryId/EmployeeTerritory', loadChildren: () => import('../EmployeeTerritory/EmployeeTerritory.module').then(m => m.EmployeeTerritoryModule),
    data: {
        oPermission: {
            permissionId: 'EmployeeTerritory-detail-permissions'
        }
    }
}
];

export const TERRITORY_MODULE_DECLARATIONS = [
    TerritoryHomeComponent,
    TerritoryNewComponent,
    TerritoryDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TerritoryRoutingModule { }