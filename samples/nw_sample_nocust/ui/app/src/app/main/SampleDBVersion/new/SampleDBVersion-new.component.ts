import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'SampleDBVersion-new',
  templateUrl: './SampleDBVersion-new.component.html',
  styleUrls: ['./SampleDBVersion-new.component.scss']
})
export class SampleDBVersionNewComponent {
  @ViewChild("SampleDBVersionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}