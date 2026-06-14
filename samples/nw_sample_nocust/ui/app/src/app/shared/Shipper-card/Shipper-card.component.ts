import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Shipper-card.component.html',
  styleUrls: ['./Shipper-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Shipper-card]': 'true'
  }
})

export class ShipperCardComponent {


}