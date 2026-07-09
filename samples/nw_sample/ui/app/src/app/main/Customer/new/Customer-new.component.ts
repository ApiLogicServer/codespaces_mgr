import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Customer-new',
  templateUrl: './Customer-new.component.html',
  styleUrls: ['./Customer-new.component.scss']
})
export class CustomerNewComponent {
  @ViewChild("CustomerForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'OrderCount': '0', 'UnpaidOrderCount': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}