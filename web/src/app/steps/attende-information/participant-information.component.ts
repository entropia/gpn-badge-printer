import {AfterViewInit, Component, OnInit} from '@angular/core';
import {InfoService} from '../../services/info.service';
import {PreviewService} from '../../services/preview.service';
import {FormCreationService} from '../../services/form-creation.service';
import {DomSanitizer} from '@angular/platform-browser';
import {FormGroup} from '@angular/forms';
import {AppState} from '../../state/app.state';
import {Router} from '@angular/router';

@Component({
  templateUrl: 'participant-information.component.html',
  styleUrls: []
})
export class ParticipantInformationComponent implements OnInit, AfterViewInit {
  form!: FormGroup;
  fields: any[] = [];

  constructor(
    private infoService: InfoService,
    private previewService: PreviewService,
    private formCreationService: FormCreationService,
    private sanitizer: DomSanitizer,
    private state: AppState,
    private router: Router,
  ) {
  }

  ngOnInit() {
    this.state.imagePreview = '';
    this.state.fields = [];

    this.getFields();
  }

  ngAfterViewInit() {
    document.getElementsByTagName('input')[0].focus();
  }

  getFields() {
    this.infoService.getFields().subscribe((fields) => {
      this.fields = fields;
      this.form = this.formCreationService.toFormGroup(fields);
    });
  }

  sendData() {
    this.previewService.getPreview(this.form.value).subscribe((preview) => {
      this.state.fields = preview.fields;
      this.state.imagePreview = this.sanitizer.bypassSecurityTrustResourceUrl(preview.image);

      this.router.navigate(['preview']);
    });
  }
}
