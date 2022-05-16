import {NgModule} from '@angular/core';
import {ShortcutComponent} from './shortcut/shortcut.component';
import {CommonModule} from '@angular/common';

@NgModule({
  declarations: [ShortcutComponent],
  imports: [
    CommonModule
  ],
  exports: [ShortcutComponent]
})
export class ComponentsModule {}
