import {NgModule} from '@angular/core';
import {ParticipantInformationComponent} from './attende-information/participant-information.component';
import {ReactiveFormsModule} from '@angular/forms';
import {PreviewComponent} from './preview/preview.component';
import {CommonModule} from '@angular/common';
import {ImageModule} from 'primeng/image';
import {PrintComponent} from './print/print.component';
import {ConfirmDialogModule} from 'primeng/confirmdialog';

@NgModule({
  declarations: [ParticipantInformationComponent, PreviewComponent, PrintComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ImageModule,
    ConfirmDialogModule,
  ],
  exports: [ParticipantInformationComponent, PreviewComponent, PrintComponent]
})
export class AppStepsModule {
}
