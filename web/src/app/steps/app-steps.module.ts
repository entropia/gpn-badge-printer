import {NgModule} from '@angular/core';
import {ParticipantInformationComponent} from './attende-information/participant-information.component';
import {ReactiveFormsModule} from '@angular/forms';
import {PreviewComponent} from './preview/preview.component';
import {CommonModule} from '@angular/common';
import {ImageModule} from 'primeng/image';
import {PrintComponent} from './print/print.component';
import {ConfirmDialogModule} from 'primeng/confirmdialog';
import {DividerModule} from 'primeng/divider';
import {InputTextModule} from 'primeng/inputtext';
import {ToastModule} from 'primeng/toast';
import {ComponentsModule} from '../components/components.module';

@NgModule({
  declarations: [ParticipantInformationComponent, PreviewComponent, PrintComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ImageModule,
    ConfirmDialogModule,
    DividerModule,
    InputTextModule,
    ToastModule,
    ComponentsModule,
  ],
  exports: [ParticipantInformationComponent, PreviewComponent, PrintComponent]
})
export class AppStepsModule {
}
