import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Territory-new',
  templateUrl: './Territory-new.component.html',
  styleUrls: ['./Territory-new.component.scss']
})
export class TerritoryNewComponent {
  @ViewChild("TerritoryForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}