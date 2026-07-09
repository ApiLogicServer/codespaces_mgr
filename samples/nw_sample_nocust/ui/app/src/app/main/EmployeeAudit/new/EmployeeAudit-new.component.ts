import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'EmployeeAudit-new',
  templateUrl: './EmployeeAudit-new.component.html',
  styleUrls: ['./EmployeeAudit-new.component.scss']
})
export class EmployeeAuditNewComponent {
  @ViewChild("EmployeeAuditForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}