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
      this.startPrint();
    }

    if (ke.code === 'Escape') {
      this.abortPrint();
    }
  }

  constructor(private state: AppState, private router: Router) {
    this.appState = state;

    document.addEventListener('keydown', this.keyboardEventListeners);
  }

  startPrint() {
    this.router.navigate(['print']);
  }

  abortPrint() {
    this.router.navigate(['']);
  }

  ngOnInit() {
    this.imageValue = this.state.imagePreview;
  }

  ngOnDestroy() {
    document.removeEventListener('keydown', this.keyboardEventListeners)
  }
}
