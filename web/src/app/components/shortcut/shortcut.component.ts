import {Component, Input} from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-shortcut',
  templateUrl: 'shortcut.component.html',
  styleUrls: ['shortcut.component.scss']
})
export class ShortcutComponent {
  @Input() direction!: Direction;
  @Input() action!: () => void;
  Direction = Direction;

  constructor(private router: Router) {
  }
}

export enum Direction {
  prev,
  next
}
