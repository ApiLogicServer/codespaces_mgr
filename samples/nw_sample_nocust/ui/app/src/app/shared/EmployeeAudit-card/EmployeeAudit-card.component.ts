import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './EmployeeAudit-card.component.html',
  styleUrls: ['./EmployeeAudit-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.EmployeeAudit-card]': 'true'
  }
})

export class EmployeeAuditCardComponent {


}