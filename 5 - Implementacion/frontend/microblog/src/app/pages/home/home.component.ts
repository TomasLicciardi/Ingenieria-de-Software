import { Component, ElementRef } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  constructor(private router: Router, private elementRef: ElementRef) {}

  scrollToSobreNosotros() {
    this.router.navigate(['/'], { fragment: 'sobrenosotros' });

    const element = this.elementRef.nativeElement.querySelector('#sobrenosotros');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  }
}

