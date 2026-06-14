import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Employee-new',
  templateUrl: './Employee-new.component.html',
  styleUrls: ['./Employee-new.component.scss']
})
export class EmployeeNewComponent {
  @ViewChild("EmployeeForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'EmployeeType': 'Salaried'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}