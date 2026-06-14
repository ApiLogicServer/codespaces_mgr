import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {CUSTOMERDEMOGRAPHIC_MODULE_DECLARATIONS, CustomerDemographicRoutingModule} from  './CustomerDemographic-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    CustomerDemographicRoutingModule
  ],
  declarations: CUSTOMERDEMOGRAPHIC_MODULE_DECLARATIONS,
  exports: CUSTOMERDEMOGRAPHIC_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class CustomerDemographicModule { }