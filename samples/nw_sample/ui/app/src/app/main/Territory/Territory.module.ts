import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TERRITORY_MODULE_DECLARATIONS, TerritoryRoutingModule} from  './Territory-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TerritoryRoutingModule
  ],
  declarations: TERRITORY_MODULE_DECLARATIONS,
  exports: TERRITORY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TerritoryModule { }