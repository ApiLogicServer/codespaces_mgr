import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SampleDBVersionHomeComponent } from './home/SampleDBVersion-home.component';
import { SampleDBVersionNewComponent } from './new/SampleDBVersion-new.component';
import { SampleDBVersionDetailComponent } from './detail/SampleDBVersion-detail.component';

const routes: Routes = [
  {path: '', component: SampleDBVersionHomeComponent},
  { path: 'new', component: SampleDBVersionNewComponent },
  { path: ':Id', component: SampleDBVersionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'SampleDBVersion-detail-permissions'
      }
    }
  }
];

export const SAMPLEDBVERSION_MODULE_DECLARATIONS = [
    SampleDBVersionHomeComponent,
    SampleDBVersionNewComponent,
    SampleDBVersionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SampleDBVersionRoutingModule { }