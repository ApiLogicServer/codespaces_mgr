import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './OrderDetail-card.component.html',
  styleUrls: ['./OrderDetail-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.OrderDetail-card]': 'true'
  }
})

export class OrderDetailCardComponent {


}