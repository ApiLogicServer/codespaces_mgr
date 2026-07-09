import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Location-card.component.html',
  styleUrls: ['./Location-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Location-card]': 'true'
  }
})

export class LocationCardComponent {


}