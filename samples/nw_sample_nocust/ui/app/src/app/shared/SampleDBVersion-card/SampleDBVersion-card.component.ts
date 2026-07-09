import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './SampleDBVersion-card.component.html',
  styleUrls: ['./SampleDBVersion-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.SampleDBVersion-card]': 'true'
  }
})

export class SampleDBVersionCardComponent {


}