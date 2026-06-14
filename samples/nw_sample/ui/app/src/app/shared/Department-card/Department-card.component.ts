import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Department-card.component.html',
  styleUrls: ['./Department-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Department-card]': 'true'
  }
})

export class DepartmentCardComponent {


}