import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Department-new',
  templateUrl: './Department-new.component.html',
  styleUrls: ['./Department-new.component.scss']
})
export class DepartmentNewComponent {
  @ViewChild("DepartmentForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'SecurityLevel': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}