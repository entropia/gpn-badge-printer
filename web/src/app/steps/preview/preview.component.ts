import {Component, OnDestroy, OnInit} from '@angular/core';
import {AppState} from '../../state/app.state';
import {Router} from '@angular/router';
import {Direction} from '../../components/shortcut/shortcut.component';

@Component({
  templateUrl: 'preview.component.html',
  styleUrls: ['preview.component.scss']
})
export class PreviewComponent implements OnInit, OnDestroy {
  imageValue: any = '';
  appState!: AppState;
  Direction = Direction;

  private keyboardEventListeners = (ke: KeyboardEvent) => {
    console.log(ke);
    if (ke.code === 'Enter') {
      this.router.navigate(['print']);
    }

    if (ke.code === 'Escape') {
      this.router.navigate(['']);
    }
  }

  constructor(private state: AppState, private router: Router) {
    this.appState = state;

    document.addEventListener('keydown', this.keyboardEventListeners);
  }

  ngOnInit() {
    this.imageValue = this.state.imagePreview;
  }

  ngOnDestroy() {
    document.removeEventListener('keydown', this.keyboardEventListeners)
  }
}
