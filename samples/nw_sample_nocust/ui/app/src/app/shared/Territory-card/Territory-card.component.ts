import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Territory-card.component.html',
  styleUrls: ['./Territory-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Territory-card]': 'true'
  }
})

export class TerritoryCardComponent {


}