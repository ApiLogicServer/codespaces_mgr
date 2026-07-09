import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {DEPARTMENT_MODULE_DECLARATIONS, DepartmentRoutingModule} from  './Department-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    DepartmentRoutingModule
  ],
  declarations: DEPARTMENT_MODULE_DECLARATIONS,
  exports: DEPARTMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class DepartmentModule { }