import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'OrderDetail-new',
  templateUrl: './OrderDetail-new.component.html',
  styleUrls: ['./OrderDetail-new.component.scss']
})
export class OrderDetailNewComponent {
  @ViewChild("OrderDetailForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Quantity': '1', 'Discount': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}