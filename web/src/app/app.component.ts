import {Component, OnInit} from '@angular/core';
import {MenuItem} from 'primeng/api';
import {Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  steps!: MenuItem[];

  constructor(private router: Router) {
  }

  ngOnInit() {
    this.steps = [
      {
        label: 'Participant',
        routerLink: 'participant'
      },
      {
        label: 'Preview',
        routerLink: 'preview'
      },
      {
        label: 'Print',
        routerLink: 'print'
      },
    ];

    this.initKeyboardShortcuts();
  }

  private initKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
      if (event.ctrlKey && event.code === 'Digit1' || event.ctrlKey && event.key === 'r') {
        this.router.navigate(['/']);
      }
    });
  }
}
