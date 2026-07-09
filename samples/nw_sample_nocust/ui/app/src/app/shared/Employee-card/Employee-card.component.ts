import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Employee-card.component.html',
  styleUrls: ['./Employee-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Employee-card]': 'true'
  }
})

export class EmployeeCardComponent {


}