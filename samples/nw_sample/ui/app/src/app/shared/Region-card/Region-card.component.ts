import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Region-card.component.html',
  styleUrls: ['./Region-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Region-card]': 'true'
  }
})

export class RegionCardComponent {


}