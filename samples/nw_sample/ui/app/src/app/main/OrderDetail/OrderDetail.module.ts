import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ORDERDETAIL_MODULE_DECLARATIONS, OrderDetailRoutingModule} from  './OrderDetail-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    OrderDetailRoutingModule
  ],
  declarations: ORDERDETAIL_MODULE_DECLARATIONS,
  exports: ORDERDETAIL_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class OrderDetailModule { }