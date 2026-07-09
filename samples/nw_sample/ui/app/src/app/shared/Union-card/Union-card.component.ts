import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Union-card.component.html',
  styleUrls: ['./Union-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Union-card]': 'true'
  }
})

export class UnionCardComponent {


}