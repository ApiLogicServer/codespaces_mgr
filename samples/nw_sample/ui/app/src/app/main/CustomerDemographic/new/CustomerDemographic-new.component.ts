import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'CustomerDemographic-new',
  templateUrl: './CustomerDemographic-new.component.html',
  styleUrls: ['./CustomerDemographic-new.component.scss']
})
export class CustomerDemographicNewComponent {
  @ViewChild("CustomerDemographicForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}