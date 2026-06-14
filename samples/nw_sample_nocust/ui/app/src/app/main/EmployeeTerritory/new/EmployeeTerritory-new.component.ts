import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'EmployeeTerritory-new',
  templateUrl: './EmployeeTerritory-new.component.html',
  styleUrls: ['./EmployeeTerritory-new.component.scss']
})
export class EmployeeTerritoryNewComponent {
  @ViewChild("EmployeeTerritoryForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}