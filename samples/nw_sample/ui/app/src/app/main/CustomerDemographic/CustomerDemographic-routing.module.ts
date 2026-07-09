import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CustomerDemographicHomeComponent } from './home/CustomerDemographic-home.component';
import { CustomerDemographicNewComponent } from './new/CustomerDemographic-new.component';
import { CustomerDemographicDetailComponent } from './detail/CustomerDemographic-detail.component';

const routes: Routes = [
  {path: '', component: CustomerDemographicHomeComponent},
  { path: 'new', component: CustomerDemographicNewComponent },
  { path: ':Id', component: CustomerDemographicDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CustomerDemographic-detail-permissions'
      }
    }
  }
];

export const CUSTOMERDEMOGRAPHIC_MODULE_DECLARATIONS = [
    CustomerDemographicHomeComponent,
    CustomerDemographicNewComponent,
    CustomerDemographicDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CustomerDemographicRoutingModule { }