import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Category-card.component.html',
  styleUrls: ['./Category-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Category-card]': 'true'
  }
})

export class CategoryCardComponent {


}