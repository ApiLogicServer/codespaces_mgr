import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './EmployeeTerritory-card.component.html',
  styleUrls: ['./EmployeeTerritory-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.EmployeeTerritory-card]': 'true'
  }
})

export class EmployeeTerritoryCardComponent {


}