import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-shortcut',
  templateUrl: 'shortcut.component.html',
  styleUrls: ['shortcut.component.scss']
})
export class ShortcutComponent {
  @Input() direction!: Direction;
  Direction = Direction;
}

export enum Direction {
  prev,
  next
}
