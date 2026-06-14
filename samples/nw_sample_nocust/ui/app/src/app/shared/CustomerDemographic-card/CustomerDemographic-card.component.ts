import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './CustomerDemographic-card.component.html',
  styleUrls: ['./CustomerDemographic-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.CustomerDemographic-card]': 'true'
  }
})

export class CustomerDemographicCardComponent {


}