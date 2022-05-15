import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ParticipantInformationComponent} from './steps/attende-information/participant-information.component';
import {PreviewComponent} from './steps/preview/preview.component';
import {PrintComponent} from './steps/print/print.component';

const routes: Routes = [
  {path: '', component: ParticipantInformationComponent},
  {path: 'preview', component: PreviewComponent},
  {path: 'print', component: PrintComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
