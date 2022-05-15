import {Component, OnInit} from '@angular/core';
import {AppState} from '../../state/app.state';
import {Router} from '@angular/router';

@Component({
  templateUrl: 'preview.component.html',
  styleUrls: ['preview.component.scss']
})
export class PreviewComponent implements OnInit {
  imageValue: any = '';
  appState!: AppState;

  constructor(private state: AppState, private router: Router) {
    this.appState = state;

    document.addEventListener('keydown', (ke) => {
      if (ke.code === 'Enter') {
        this.router.navigate(['print']);
      }
    });
  }

  ngOnInit() {
    this.imageValue = this.state.imagePreview;
  }
}
